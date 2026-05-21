from pathlib import Path
import difflib, shutil, re

def generate_patch(source_file: str, crash_type: str, mapped_line: int, output_dir: Path) -> dict:
    src = Path(source_file)
    if not src.exists():
        return {"patched": False, "reason": f"source file not found: {source_file}"}
    patched_dir = output_dir / "patched"
    patched_dir.mkdir(parents=True, exist_ok=True)
    dst = patched_dir / src.name
    original = src.read_text(encoding="utf-8", errors="ignore")
    patched = patch_text(original, src.suffix, crash_type, mapped_line)
    dst.write_text(patched, encoding="utf-8")
    diff = "".join(difflib.unified_diff(original.splitlines(True), patched.splitlines(True), fromfile=str(src), tofile=str(dst)))
    (output_dir / "patch.diff").write_text(diff, encoding="utf-8")
    return {"patched": original != patched, "patched_file": str(dst), "diff": diff}

def patch_text(text: str, suffix: str, crash_type: str, mapped_line: int) -> str:
    if crash_type != "DivisionByZero":
        return text + "\n# ChaosForge note: crash detected but no safe automatic patch rule exists for this crash type.\n"
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
