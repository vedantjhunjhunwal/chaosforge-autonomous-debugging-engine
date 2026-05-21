import json, subprocess, sys

def test_normal_case():
    cp = subprocess.run([sys.executable, "examples/python_cli/finance_cli.py", '{"amount":100,"price":5}'], capture_output=True, text=True)
    assert cp.returncode == 0
