from pathlib import Path
import json, yaml
from chaosforge.schemas import TargetContract

def load_contract(path: str | Path) -> TargetContract:
    p = Path(path)
    data = p.read_text(encoding="utf-8")
    raw = yaml.safe_load(data) if p.suffix.lower() in {".yaml", ".yml"} else json.loads(data)
    if "contract" in raw:
        raw = raw["contract"]
    return TargetContract(**raw)
