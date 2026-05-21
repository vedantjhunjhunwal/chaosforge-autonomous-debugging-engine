# ChaosForge Production App

ChaosForge is a production-style autonomous debugging platform for executable software targets. It keeps the original ChaosForge debugging architecture:

```text
Adversary -> Fuzzing Sandbox -> Crash Check -> Code Surgeon -> Monte Carlo CI Sandbox -> Final Compiler
```

But it runs as a real application with:

- FastAPI backend
- JWT authentication
- SQLite by default, PostgreSQL-ready via `DATABASE_URL`
- Persistent run history
- Background worker execution
- Universal target contracts
- CLI and REST API
- Local dashboard
- Artifact storage per run
- Patch diff generation
- Regression test generation
- Monte Carlo verification
- Docker and docker-compose
- Pytest suite
- GitHub Actions CI

## 1. Quick start

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
python -m chaosforge.db.init_db
python apps.py create-user --email admin@example.com --password admin123 --name Admin
python apps.py serve
```

Open:

```text
http://127.0.0.1:8000
```

Login token from CLI:

```bash
python apps.py login --email admin@example.com --password admin123
```

## 2. Run built-in demo from CLI

```bash
python apps.py run --contract contracts/python_demo.json --email admin@example.com --password admin123 --runs 10 --concurrency 2
```

Expected result:

```text
status: completed
crash_found: true
patch.diff generated
PR_DESCRIPTION.md generated
```

## 3. Universal target contract

ChaosForge is language-agnostic. It does not need to know whether the target is Python, Java, C, C++, Rust, Go, Node, or something else.

It only needs this contract:

```json
{
  "name": "python-finance-demo",
  "mode": "command",
  "workdir": ".",
  "build_command": "",
  "run_command": "python examples/python_cli/finance_cli.py '{payload}'",
  "test_command": "python examples/python_cli/test_finance.py",
  "source_files": ["examples/python_cli/finance.py"],
  "payload_channel": "argv",
  "timeout_seconds": 5,
  "success_exit_code": 0
}
```

For C/C++/Java use compile-run:

```json
{
  "name": "c-demo",
  "mode": "compile-run",
  "workdir": "examples/c_cli",
  "build_command": "gcc main.c -o main",
  "run_command": "./main '{payload}'",
  "test_command": "./test.sh",
  "source_files": ["examples/c_cli/main.c"],
  "payload_channel": "argv",
  "timeout_seconds": 5,
  "success_exit_code": 0
}
```

## 4. REST API

Start server:

```bash
python apps.py serve
```

Register/login:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

Create run:

```bash
curl -X POST http://127.0.0.1:8000/api/runs \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d @contracts/python_demo.json
```

## 5. Docker

```bash
docker compose up --build
```

Then visit:

```text
http://127.0.0.1:8000
```

## 6. Generated artifacts

Each run writes artifacts to:

```text
artifacts/runs/<run_id>/
  contract.json
  repository_scan.json
  payloads.json
  crash_result.json
  crash_trace.txt
  patch.diff
  patched/
  generated_tests/regression.sh
  monte_carlo_report.json
  PR_DESCRIPTION.md
  final_report.json
```

## 7. Honest production boundary

This app includes production-style engineering: API, auth, persistence, worker, dashboard, Docker, CI, testing, and artifacts. In a real enterprise deployment you would still harden the execution sandbox with Firecracker/gVisor/Kubernetes namespaces, replace SQLite with PostgreSQL, and plug in real LLM/provider credentials for deeper patch synthesis.
