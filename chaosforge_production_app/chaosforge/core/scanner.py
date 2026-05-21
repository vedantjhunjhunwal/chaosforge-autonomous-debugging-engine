from pathlib import Path
import hashlib

TEXT_EXTS = {".py", ".c", ".cpp", ".cc", ".h", ".hpp", ".java", ".js", ".ts", ".go", ".rs", ".rb", ".php"}

def scan_repository(workdir: str, source_files: list[str]) -> dict:
    base = Path(workdir).resolve()
    files = []
    targets = [Path(f) for f in source_files] if source_files else list(base.rglob("*"))
    for f in targets:
        p = (base / f).resolve() if not f.is_absolute() else f.resolve()
        if p.is_file() and p.suffix in TEXT_EXTS:
            try:
                content = p.read_text(encoding="utf-8", errors="ignore")
                files.append({
                    "path": str(p),
                    "relative_path": str(p.relative_to(base)) if str(p).startswith(str(base)) else str(p),
                    "language": language_for(p),
                    "lines": content.count("\n") + 1,
                    "sha256": hashlib.sha256(content.encode("utf-8", errors="ignore")).hexdigest(),
                })
            except Exception as e:
                files.append({"path": str(p), "error": str(e)})
    return {"workdir": str(base), "files": files, "file_count": len(files)}

def language_for(p: Path) -> str:
    return {".py":"python", ".c":"c", ".cpp":"cpp", ".cc":"cpp", ".java":"java", ".js":"javascript", ".ts":"typescript", ".go":"go", ".rs":"rust"}.get(p.suffix, "unknown")
