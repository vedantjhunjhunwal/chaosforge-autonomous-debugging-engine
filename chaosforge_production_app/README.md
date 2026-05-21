# ChaosForge — Autonomous Debugging & Reliability Engine

> A production-style autonomous debugging app that attacks executable software targets, detects runtime failures, maps crashes to source code, generates patch/test artifacts, validates fixes through Monte Carlo CI, and produces PR-ready reports for human review.

---

## What is ChaosForge?

ChaosForge is an **autonomous debugging and reliability engine**.

In simple words:

Imagine you have a backend function, CLI program, API service, C/C++ binary, Java program, Python app, or any executable system.

Normally, when it fails, an engineer has to:

1. Reproduce the bug.
2. Try edge-case inputs.
3. Read the stack trace.
4. Find the broken file.
5. Patch the code.
6. Write a regression test.
7. Run the test many times.
8. Check if the fix is stable.
9. Write a PR summary.

ChaosForge automates this workflow.

It acts like an autonomous debugging teammate that can:

- Generate adversarial inputs.
- Run the target program in a sandbox.
- Detect crashes, timeouts, bad exits, and test failures.
- Map failures back to source files.
- Generate patch artifacts.
- Generate regression test artifacts.
- Run repeated Monte Carlo CI validation.
- Produce a PR-style report for a human engineer.

This project is designed as an **AI Agent + Software Engineering + Testing Infrastructure project**.

---

## Why This Project Matters

Modern software fails in many hidden ways.

A small bug can cause:

- Division-by-zero crashes
- Invalid input failures
- Runtime exceptions
- Segmentation faults
- Timeout failures
- Incorrect edge-case behavior
- Flaky tests
- Broken CLI/API workflows
- Poor reliability under stress

Traditional AI projects only generate code from prompts.

ChaosForge goes further.

It connects AI-style reasoning with real engineering execution:

- Fuzzing
- Sandboxed execution
- Crash analysis
- Source-code scanning
- Patch generation
- Test generation
- CI-style repeated validation
- PR artifact creation

This makes the project closer to how real developer tooling and reliability systems work.

---

## Core Idea

```text
Target Program
      ↓
Adversary Agent
      ↓
Fuzzing Sandbox
      ↓
Crash Check Router
      ↓
Code Surgeon
      ↓
Monte Carlo CI Sandbox
      ↓
Flake Check Router
      ↓
Final Compiler
      ↓
PR-ready Report
```

ChaosForge does not blindly generate code.

It follows a structured, verification-based workflow:

1. Understand the target contract.
2. Generate extreme inputs.
3. Execute the target.
4. Capture failure evidence.
5. Map crash evidence to code.
6. Generate a patch artifact.
7. Generate a regression test artifact.
8. Run the validation repeatedly.
9. Produce a final PR report.

---

## Architecture

```text
 [ Input: Universal Target Contract ]
 [ Python / Java / C / C++ / JS / Go / Rust / API / CLI / Docker / Repo ]
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ Node 1: The Adversary                                  │
  │ Generates extreme payloads, malformed files, CLI args, │
  │ HTTP requests, or stdin inputs                         │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ Node 2: The Fuzzing Sandbox                            │
  │ Executes payloads against the target using its adapter:│
  │ command / stdin / file / http / compile-run / repo-test│
  └──────────────────────────┬─────────────────────────────┘
                             │
                   [ Router 1: Crash Check ]
               /                              \
  [ NO: Code survived ]                [ YES: Code crashed ]
               │                                │
               │                                ▼
               │        ┌────────────────────────────────────────┐
               │        │ Node 3: The Code Surgeon               │
               │        │ Reads stderr, stack trace, timeout,    │
               │        │ crash logs, compiler output, or failed │
               │        │ test output. Generates patch/test      │
               │        │ artifacts.                             │
               │        └──────────────────┬─────────────────────┘
               │                           │
               │                           ▼
               │        ┌────────────────────────────────────────┐
               │        │ Node 4: Monte Carlo CI Sandbox         │
               │        │ Runs validation many times concurrently│
               │        │ to detect flakes or unstable fixes     │
               │        └──────────────────┬─────────────────────┘
               │                           │
               │                 [ Router 2: Flake Check ]
               │              /                             \
               │ [ Failed on run #42 ]             [ 100/100 Passes ]
               │              │                             │
               └──────────────┘                             ▼
                           ┌────────────────────────────────────────┐
                           │ Node 5: Final Compiler                 │
                           │ Outputs bug report, patch diff,        │
                           │ regression evidence, CI summary, and   │
                           │ PR-ready markdown artifact             │
                           └────────────────────────────────────────┘
```

---

## Technical Stack

| Area | Technology |
|---|---|
| Backend | Python |
| API Layer | FastAPI |
| CLI | argparse / Python CLI |
| Database | SQLite |
| Auth | JWT-style local auth |
| Contract Format | JSON |
| Sandbox Execution | subprocess |
| Testing | pytest / target-specific test command |
| CI Validation | Monte Carlo repeated execution |
| Reports | Markdown + JSON artifacts |
| External Targets | Python, C, C++, Java, Node, Go, Rust, CLI tools, HTTP APIs |
| Deployment | Local Python, Docker-ready structure |

---

## What ChaosForge Fixes in the Demo

The demo target contains a common production-style bug:

```python
def calculate_margin(balance, leverage, price):
    return balance * leverage / price
```

If `price = 0`, the system crashes with:

```text
ZeroDivisionError
```

ChaosForge attacks the function with adversarial inputs, detects the crash, maps the failure to the source file, generates a patch artifact, creates a regression test artifact, runs repeated validation, and writes a PR-style report.

Example hardened logic:

```python
def calculate_margin(balance, leverage, price):
    if price == 0:
        return 0
    return balance * leverage / price
```

---

## Project Features

### 1. Universal Target Contracts

ChaosForge does not depend on one language.

It can test any target that can be described with:

```text
build command + run command + test command + input mode + timeout
```

Example:

```json
{
  "name": "python-demo",
  "mode": "command",
  "workdir": "examples/python_cli",
  "build_command": "",
  "run_command": "python app.py {payload}",
  "test_command": "python -m pytest",
  "input_mode": "argv",
  "source_roots": ["."],
  "timeout_seconds": 5
}
```

---

### 2. Adversarial Payload Generation

The Adversary node creates edge-case inputs such as zero values, negative values, very large numbers, empty strings, malformed JSON, nested structures, boundary values, and invalid file payloads.

---

### 3. Fuzzing Sandbox

The Fuzzing Sandbox runs the target with generated payloads and captures stdout, stderr, exit code, timeout status, failing payload, crash trace, build failures, and test failures.

---

### 4. Crash-to-File Mapping

ChaosForge scans source files and tries to map the observed crash to the most likely file and line.

Example output:

```json
{
  "mapped_file": "examples/python_cli/finance.py",
  "mapped_line": 4,
  "crash_type": "DivisionByZero"
}
```

---

### 5. Patch Diff Generation

ChaosForge generates a patch artifact:

```text
artifacts/runs/<run_id>/patch.diff
```

This is important because it gives a real engineering artifact, not just a natural language explanation.

---

### 6. Regression Test Generation

ChaosForge creates regression test artifacts inside:

```text
artifacts/runs/<run_id>/generated_tests/
```

The goal is to preserve the failing case so the bug does not return later.

---

### 7. Monte Carlo CI Validation

A normal test run can pass once and still be flaky.

ChaosForge runs the validation repeatedly:

```text
Run 1 passed
Run 2 passed
Run 3 passed
...
Run 100 passed
```

If any run fails, it records the failure and marks the fix as unstable.

---

### 8. PR Artifact Generation

ChaosForge generates:

```text
artifacts/runs/<run_id>/PR_DESCRIPTION.md
```

The PR artifact includes incident summary, failing payload, crash evidence, mapped source location, patch summary, test results, Monte Carlo CI result, and a human review note.

---

### 9. Web Dashboard

ChaosForge includes a local dashboard for viewing runs.

Run:

```bash
python apps.py serve
```

Open:

```text
http://127.0.0.1:8000
```

The dashboard helps show the app as a product instead of only a script.

---

## How to Run Locally on Windows

### Step 1: Clone the repository

```cmd
git clone https://github.com/YOUR_USERNAME/chaosforge-autonomous-debugging-engine.git
cd chaosforge-autonomous-debugging-engine
```

### Step 2: Create virtual environment

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install dependencies

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Initialize database

```cmd
python -m chaosforge.db.init_db
```

### Step 5: Run the built-in Python demo

```cmd
python apps.py run --contract contracts\python_demo.json --runs 10 --concurrency 2 --no-auth
```

Expected output:

```json
{
  "status": "completed",
  "crash_found": true,
  "patch_generated": true
}
```

---

## How to Run on macOS / Linux

```bash
git clone https://github.com/YOUR_USERNAME/chaosforge-autonomous-debugging-engine.git
cd chaosforge-autonomous-debugging-engine

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

python3 -m chaosforge.db.init_db
python3 apps.py run --contract contracts/python_demo.json --runs 10 --concurrency 2 --no-auth
```

---

## Running the Dashboard

```bash
python apps.py serve
```

Open:

```text
http://127.0.0.1:8000
```

---

## Testing With C / C++ / External Repositories

For C projects, you need build tools.

On Windows, install MSYS2, MinGW, gcc, and make.

On WSL Ubuntu:

```bash
sudo apt update
sudo apt install -y git make gcc g++ python3 python3-venv python3-pip
```

Example C contract:

```json
{
  "name": "c-demo",
  "mode": "compile-run",
  "workdir": "examples/c_cli",
  "build_command": "gcc main.c -o main",
  "run_command": "./main {payload}",
  "test_command": "./test.sh",
  "input_mode": "argv",
  "source_roots": ["."],
  "timeout_seconds": 5
}
```

Run:

```bash
python apps.py run --contract contracts/c_demo.json --runs 10 --concurrency 2 --no-auth
```

---

## Testing With Fuzzgoat

Fuzzgoat is a deliberately vulnerable C program used for fuzzing experiments.

Clone it beside ChaosForge:

```bash
git clone https://github.com/fuzzstati0n/fuzzgoat.git
```

Folder structure:

```text
chaosforge-test-lab/
  chaosforge_production_app/
  fuzzgoat/
```

Create:

```text
contracts/fuzzgoat.json
```

Content:

```json
{
  "name": "fuzzgoat",
  "mode": "compile-run",
  "workdir": "../fuzzgoat",
  "build_command": "make",
  "run_command": "./fuzzgoat {payload_file}",
  "test_command": "./fuzzgoat .chaosforge_input.txt",
  "input_mode": "file",
  "source_roots": ["."],
  "timeout_seconds": 5
}
```

Run:

```bash
python apps.py run --contract contracts/fuzzgoat.json --runs 20 --concurrency 4 --no-auth
```

If Windows shows `make is not recognized`, ChaosForge is working, but your system does not have the C build tool installed. Use WSL or install MSYS2/MinGW.

---

## Generated Artifacts

Every run creates a folder:

```text
artifacts/runs/<run_id>/
```

Inside it:

```text
repository_scan.json
build_result.json
payloads.json
failing_payload.json
crash_result.json
crash_trace.txt
patch.diff
generated_tests/
monte_carlo_report.json
chaosforge_report.json
PR_DESCRIPTION.md
```

The most important files are:

```text
patch.diff
PR_DESCRIPTION.md
chaosforge_report.json
```

These prove that the system executed the target and produced engineering artifacts.

---

## Example Workflow Output

```text
load_contract → Target contract loaded
scan_repository → Source files discovered
build_target → Build command executed
generate_payloads → Adversarial inputs generated
fuzz_target → Target executed with payloads
crash_check → Crash detected
map_crash → Crash mapped to source file
generate_patch → Patch artifact created
generate_test → Regression test artifact created
monte_carlo_ci → Repeated validation passed
final_compile → PR report generated
```

Final status:

```text
completed
```

---

## Repository Structure

```text
chaosforge-autonomous-debugging-engine/
│
├── apps.py
├── requirements.txt
├── README.md
├── Dockerfile
├── docker-compose.yml
│
├── chaosforge/
│   ├── cli.py
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── dashboard/
│   ├── security/
│   └── workers/
│
├── contracts/
│   ├── python_demo.json
│   ├── c_demo.json
│   └── fuzzgoat.json
│
├── examples/
│   ├── python_cli/
│   └── c_cli/
│
├── tests/
│
└── artifacts/
    └── runs/
```

---

## Why This Is More Than a Basic AI Project

A basic AI project usually works like this:

```text
Prompt → LLM → Answer
```

ChaosForge works like this:

```text
Target Contract
→ Adversarial Inputs
→ Real Execution
→ Crash Evidence
→ Source Mapping
→ Patch Artifact
→ Regression Test
→ Monte Carlo CI
→ PR Report
```

This makes it a real engineering workflow.

It includes multi-step agent architecture, tool usage, state transitions, conditional routing, verification loops, real subprocess execution, source-code analysis, CI-style validation, and human-reviewable artifacts.

---

## Design Principles

### 1. Execution Over Theory

ChaosForge runs the target program. It does not only describe what might happen.

### 2. Evidence Before Patch

The system captures failing payloads, traces, stdout, stderr, and exit codes before generating reports.

### 3. Verification Over Guessing

A patch is only useful if the validation command passes repeatedly.

### 4. Universal Target Contract

The system is not tied to Python.

If a program can be built, run, and tested from a command, ChaosForge can analyze it.

### 5. Human Approval

ChaosForge produces PR-ready artifacts, but a human engineer should review before merging.



---


## License

This project is intended for educational, research, and portfolio purposes.
