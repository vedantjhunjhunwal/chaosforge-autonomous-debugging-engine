from pydantic import BaseModel, Field
from typing import Literal, Optional, List

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TargetContract(BaseModel):
    name: str = Field(..., min_length=1)
    mode: Literal["command", "compile-run", "stdin", "http"] = "command"
    workdir: str = "."
    build_command: str = ""
    run_command: str
    test_command: str = ""
    source_files: List[str] = []
    payload_channel: Literal["argv", "stdin", "http_json"] = "argv"
    timeout_seconds: int = 5
    success_exit_code: int = 0

class RunCreate(BaseModel):
    contract: TargetContract
    runs: int = 100
    concurrency: int = 8

class RunResponse(BaseModel):
    id: str
    status: str
    target_name: str
    crash_found: bool
    crash_type: str = ""
    mapped_location: str = ""
    ci_passes: int = 0
    ci_total: int = 0
    artifact_dir: str = ""
    error: str = ""
