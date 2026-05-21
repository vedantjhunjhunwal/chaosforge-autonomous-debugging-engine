import ast, re
from pathlib import Path

def parse_sources(source_files: list[str], workdir: str = ".") -> dict:
    symbols = []
    for sf in source_files:
        p = Path(workdir) / sf
        if not p.exists():
            p = Path(sf)
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if p.suffix == ".py":
            symbols.extend(parse_python(p, text))
        else:
            symbols.extend(parse_c_like(p, text))
    return {"symbols": symbols}

def parse_python(path: Path, text: str):
    out=[]
    try:
        tree=ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                out.append({"path": str(path), "name": node.name, "kind": type(node).__name__, "line": node.lineno})
    except SyntaxError as e:
        out.append({"path": str(path), "kind":"syntax_error", "line": e.lineno or 0, "name": str(e)})
    return out

def parse_c_like(path: Path, text: str):
    out=[]
    pattern = re.compile(r"^\s*(?:int|double|float|long|short|void|char|bool|public|private|static|class|func|fn)\s+([A-Za-z_][A-Za-z0-9_]*)", re.M)
    for m in pattern.finditer(text):
        line = text[:m.start()].count("\n") + 1
        out.append({"path": str(path), "name": m.group(1), "kind":"symbol", "line": line})
    return out
