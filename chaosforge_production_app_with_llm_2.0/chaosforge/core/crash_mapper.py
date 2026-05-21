import re
from pathlib import Path

def map_crash(result: dict, source_files: list[str], workdir: str = ".") -> dict:
    stderr = result.get("stderr", "") or ""
    stdout = result.get("stdout", "") or ""
    text = stderr + "\n" + stdout
    # Python traceback: File "...", line N
    py = re.findall(r'File "([^"]+)", line (\d+)', text)
    if py:
        file, line = py[-1]
        return {"file": file, "line": int(line), "confidence": 0.95, "reason": "traceback"}
    # gcc/runtime often lacks line; use known source and division heuristics
    if result.get("crash_type") == "DivisionByZero":
        for sf in source_files:
            p = Path(workdir) / sf
            if not p.exists(): p = Path(sf)
            if p.exists():
                lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
                for i, line in enumerate(lines, 1):
                    if "/" in line and not line.strip().startswith("//"):
                        return {"file": str(p), "line": i, "confidence": 0.75, "reason": "division_operator_heuristic"}
    if source_files:
        return {"file": source_files[0], "line": 1, "confidence": 0.3, "reason": "fallback_source"}
    return {"file": "", "line": 0, "confidence": 0.0, "reason": "unmapped"}
