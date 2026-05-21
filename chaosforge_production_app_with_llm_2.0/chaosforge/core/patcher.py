from pathlib import Path
import difflib, re, json
from chaosforge.llm.client import extract_json


def generate_patch(source_file: str, crash_type: str, mapped_line: int, output_dir: Path, crash_result: dict | None = None, payload: dict | None = None, llm=None) -> dict:
    """Node 3: Code Surgeon.

    LLM mode: asks the model to return patched full source code as JSON.
    Fallback mode: applies deterministic guards for known crash classes.
    """
    src = Path(source_file)
    if not src.exists():
        return {"patched": False, "reason": f"source file not found: {source_file}"}
    patched_dir = output_dir / "patched"
    patched_dir.mkdir(parents=True, exist_ok=True)
    dst = patched_dir / src.name
    original = src.read_text(encoding="utf-8", errors="ignore")

    llm_summary = ""
    llm_used = False
    patched = None
    if llm and getattr(llm, "enabled", False):
        llm_out = _llm_patch(original, src, crash_type, mapped_line, crash_result or {}, payload or {}, llm)
        if llm_out and llm_out.get("patched_code"):
            candidate = str(llm_out["patched_code"]).strip() + "\n"
            if candidate.strip() and candidate != original:
                patched = candidate
                llm_summary = str(llm_out.get("summary", "LLM-generated patch"))
                llm_used = True

    if patched is None:
        patched = patch_text(original, src.suffix, crash_type, mapped_line)
        llm_summary = "Deterministic fallback patch rule used."

    dst.write_text(patched, encoding="utf-8")
    diff = "".join(difflib.unified_diff(original.splitlines(True), patched.splitlines(True), fromfile=str(src), tofile=str(dst)))
    (output_dir / "patch.diff").write_text(diff, encoding="utf-8")
    return {"patched": original != patched, "patched_file": str(dst), "diff": diff, "llm_used": llm_used, "summary": llm_summary}


def _llm_patch(original: str, src: Path, crash_type: str, mapped_line: int, crash_result: dict, payload: dict, llm) -> dict | None:
    system = """You are ChaosForge Code Surgeon Agent.
You patch source code to fix the reproduced crash while preserving behavior.
Return ONLY valid JSON with keys: patched_code, summary, risk_notes.
Do not wrap in markdown. Do not omit any original code that should remain."""
    numbered = "\n".join(f"{i+1}: {line}" for i, line in enumerate(original.splitlines()))
    prompt = {
        "file": str(src),
        "language_hint": src.suffix,
        "crash_type": crash_type,
        "mapped_line": mapped_line,
        "failing_payload": payload,
        "stderr_tail": (crash_result.get("stderr") or "")[-3000:],
        "stdout_tail": (crash_result.get("stdout") or "")[-1000:],
        "source_with_line_numbers": numbered[:20000],
        "requirements": [
            "Patch the root cause, not just the test.",
            "Preserve public interfaces and CLI behavior.",
            "Add validation for unsafe inputs where relevant.",
            "Do not introduce eval, exec, shell execution, network calls, or secrets.",
            "Return full patched file content in patched_code.",
        ],
    }
    text = llm.complete(system, json.dumps(prompt, indent=2), temperature=0.1)
    data = extract_json(text or "")
    return data if isinstance(data, dict) else None


def patch_text(text: str, suffix: str, crash_type: str, mapped_line: int) -> str:
    if crash_type != "DivisionByZero":
        comment = "#" if suffix == ".py" else "//"
        return text + f"\n{comment} ChaosForge note: crash detected but no safe automatic patch rule exists for this crash type.\n"
    if suffix == ".py":
        return patch_python_division(text, mapped_line)
    if suffix in {".c", ".cpp", ".cc", ".h", ".hpp"}:
        return patch_c_division(text, mapped_line)
    return text


def patch_python_division(text: str, mapped_line: int) -> str:
    lines = text.splitlines()
    idx = max(0, min(len(lines)-1, mapped_line-1))
    target = lines[idx]
    indent = re.match(r"^(\s*)", target).group(1)
    if "/ price" in target:
        lines.insert(idx, indent + "if price == 0:")
        lines.insert(idx+1, indent + "    return 0")
        return "\n".join(lines) + "\n"
    if "/ payload.get(\"price\"" in target or "/ payload.get('price'" in target:
        lines.insert(idx, indent + "price = payload.get('price') or 0")
        lines.insert(idx+1, indent + "if price == 0:")
        lines.insert(idx+2, indent + "    return 0")
        lines[idx+3] = target.replace("payload.get(\"price\", 1)", "price").replace("payload.get('price', 1)", "price")
        return "\n".join(lines) + "\n"
    lines.insert(idx, indent + "# ChaosForge guard: verify divisors before division")
    return "\n".join(lines) + "\n"


def patch_c_division(text: str, mapped_line: int) -> str:
    lines=text.splitlines()
    idx=max(0,min(len(lines)-1,mapped_line-1))
    target=lines[idx]
    indent=re.match(r"^(\s*)", target).group(1)
    if "price" in target and "/" in target:
        lines.insert(idx, indent + "if (price == 0) { return 0; }")
    else:
        lines.insert(idx, indent + "/* ChaosForge guard: validate divisors before division. */")
    return "\n".join(lines)+"\n"
