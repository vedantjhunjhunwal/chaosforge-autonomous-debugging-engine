from pathlib import Path
import json
from chaosforge.llm.client import extract_json


def write_pr_artifact(output_dir: Path, report: dict, llm=None) -> str:
    md = None
    if llm and getattr(llm, "enabled", False):
        md = _llm_pr(report, output_dir, llm)
    if not md:
        md = default_pr(report)
    path = output_dir / "PR_DESCRIPTION.md"
    path.write_text(md.strip() + "\n", encoding="utf-8")
    return str(path)


def _llm_pr(report: dict, output_dir: Path, llm) -> str | None:
    patch = ""
    crash = ""
    try:
        patch = (output_dir / "patch.diff").read_text(encoding="utf-8", errors="ignore")[-8000:]
    except Exception:
        pass
    try:
        crash = (output_dir / "crash_trace.txt").read_text(encoding="utf-8", errors="ignore")[-4000:]
    except Exception:
        pass
    system = """You are ChaosForge Final Compiler Agent.
Write a concise, professional GitHub PR description for a debugging patch.
Return ONLY markdown text. Include Summary, Reproduction, Root Cause, Patch, Validation, Risk, Human Review Checklist."""
    prompt = json.dumps({"final_report": report, "crash_trace_tail": crash, "patch_diff_tail": patch}, indent=2)
    text = llm.complete(system, prompt, temperature=0.2)
    if text and len(text.strip()) > 100:
        return text.strip().replace("```markdown", "").replace("```", "").strip()
    return None


def default_pr(report: dict) -> str:
    return f"""
# ChaosForge Automated Reliability Patch

## Summary

ChaosForge reproduced a runtime failure, mapped it to source code, generated a patch artifact, created a regression test, and validated the result through Monte Carlo CI.

## Target

- Target: `{report.get('target_name')}`
- Status: `{report.get('status')}`
- Crash found: `{report.get('crash_found')}`
- Crash type: `{report.get('crash_type')}`
- Mapped location: `{report.get('mapped_location')}`
- LLM used: `{report.get('llm_used')}`

## Validation

- CI passes: `{report.get('ci_passes')}/{report.get('ci_total')}`
- Artifact directory: `{report.get('artifact_dir')}`

## Files Generated

- `patch.diff`
- `crash_trace.txt`
- `generated_tests/regression.sh`
- `monte_carlo_report.json`
- `final_report.json`

## Human Review Checklist

- [ ] Confirm patch logic is semantically correct
- [ ] Confirm regression test is meaningful
- [ ] Confirm no security-sensitive data is present in logs
- [ ] Run project-native CI before merge
"""
