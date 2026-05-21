from pathlib import Path
import json
from chaosforge.config import ARTIFACT_ROOT

def make_run_dir(run_id: str) -> Path:
    d = ARTIFACT_ROOT / "runs" / run_id
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_json(path: Path, data: dict | list):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

def write_text(path: Path, data: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")
