from pathlib import Path
import json, shlex
from chaosforge.schemas import TargetContract
from chaosforge.core.adversary import payload_to_arg

def generate_regression_test(contract: TargetContract, payload: dict, output_dir: Path) -> dict:
    tests_dir = output_dir / "generated_tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    payload_s = payload_to_arg(payload)
    if contract.test_command:
        body = f"#!/usr/bin/env bash\nset -euo pipefail\n{contract.test_command}\n"
    else:
        cmd = contract.run_command.replace("{payload}", shlex.quote(payload_s)).replace("{payload_json}", shlex.quote(payload_s))
        body = f"#!/usr/bin/env bash\nset -euo pipefail\ncd {shlex.quote(contract.workdir)}\n{cmd}\n"
    test_path = tests_dir / "regression.sh"
    test_path.write_text(body, encoding="utf-8")
    test_path.chmod(0o755)
    (tests_dir / "failing_payload.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return {"test_path": str(test_path), "payload_path": str(tests_dir / "failing_payload.json")}
