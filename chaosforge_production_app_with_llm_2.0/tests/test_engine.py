from chaosforge.core.contracts import load_contract
from chaosforge.core.engine import ChaosForgeEngine

def test_python_demo_engine_runs(tmp_path, monkeypatch):
    monkeypatch.setenv("ARTIFACT_ROOT", str(tmp_path))
    contract = load_contract("contracts/python_demo.json")
    report = ChaosForgeEngine().execute_run("testrun001", contract, runs=2, concurrency=1)
    assert report["crash_found"] is True
    assert report["crash_type"] == "DivisionByZero"
    assert report["ci_total"] == 2
