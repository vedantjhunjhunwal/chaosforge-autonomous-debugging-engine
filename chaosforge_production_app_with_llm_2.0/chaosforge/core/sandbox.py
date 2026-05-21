from dataclasses import dataclass, asdict
import subprocess, shlex, time, os, json
from pathlib import Path
import requests
from chaosforge.schemas import TargetContract
from chaosforge.core.adversary import payload_to_arg

@dataclass
class ExecResult:
    payload_id: str
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: int
    timed_out: bool = False
    crashed: bool = False
    crash_type: str = ""

    def to_dict(self):
        return asdict(self)

def render_command(template: str, payload: dict) -> str:
    payload_arg = shlex.quote(payload_to_arg(payload))
    return template.replace("{payload}", payload_arg).replace("{payload_json}", payload_arg)

def run_build(contract: TargetContract) -> ExecResult | None:
    if contract.mode == "compile-run" and contract.build_command:
        return run_shell(contract.build_command, contract.workdir, contract.timeout_seconds, "build")
    return None

def execute_payload(contract: TargetContract, payload: dict) -> ExecResult:
    if contract.mode == "http":
        return execute_http(contract, payload)
    cmd = render_command(contract.run_command, payload)
    if contract.payload_channel == "stdin":
        return run_shell(cmd, contract.workdir, contract.timeout_seconds, payload.get("id", "payload"), stdin=payload_to_arg(payload))
    return run_shell(cmd, contract.workdir, contract.timeout_seconds, payload.get("id", "payload"))

def execute_http(contract: TargetContract, payload: dict) -> ExecResult:
    start = time.time()
    try:
        r = requests.post(contract.run_command, json=payload, timeout=contract.timeout_seconds)
        dur = int((time.time()-start)*1000)
        crashed = r.status_code >= 500
        return ExecResult(payload.get("id","payload"), contract.run_command, r.status_code, r.text[:4000], "", dur, False, crashed, "HTTP5xx" if crashed else "")
    except Exception as e:
        dur = int((time.time()-start)*1000)
        return ExecResult(payload.get("id","payload"), contract.run_command, -1, "", repr(e), dur, False, True, type(e).__name__)

def run_shell(cmd: str, workdir: str, timeout: int, payload_id: str, stdin: str | None = None) -> ExecResult:
    start=time.time()
    try:
        cp = subprocess.run(cmd, input=stdin, shell=True, cwd=workdir, text=True, capture_output=True, timeout=timeout)
        dur=int((time.time()-start)*1000)
        stderr=cp.stderr or ""
        stdout=cp.stdout or ""
        crash_type = classify_failure(cp.returncode, stdout, stderr)
        crashed = cp.returncode != 0 or bool(crash_type)
        return ExecResult(payload_id, cmd, cp.returncode, stdout[-4000:], stderr[-8000:], dur, False, crashed, crash_type)
    except subprocess.TimeoutExpired as e:
        dur=int((time.time()-start)*1000)
        return ExecResult(payload_id, cmd, -9, e.stdout or "", e.stderr or "timeout", dur, True, True, "Timeout")

def classify_failure(exit_code: int, stdout: str, stderr: str) -> str:
    text = (stdout + "\n" + stderr).lower()
    if "zerodivisionerror" in text or "division by zero" in text or "floating point exception" in text:
        return "DivisionByZero"
    if "segmentation fault" in text or exit_code == 139:
        return "SegmentationFault"
    if "indexerror" in text or "out of bounds" in text:
        return "OutOfBounds"
    if "keyerror" in text:
        return "MissingKey"
    if "typeerror" in text:
        return "TypeError"
    if exit_code != 0:
        return "NonZeroExit"
    return ""
