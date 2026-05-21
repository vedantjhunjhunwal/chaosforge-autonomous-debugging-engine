from pathlib import Path

def write_pr_artifact(output_dir: Path, report: dict) -> str:
    md = f"""
# ChaosForge Automated Reliability Patch

## Summary

ChaosForge reproduced a runtime failure, mapped it to source code, generated a patch artifact, created a regression test, and validated the result through Monte Carlo CI.

## Target

- Target: `{report.get('target_name')}`
- Status: `{report.get('status')}`
- Crash found: `{report.get('crash_found')}`
- Crash type: `{report.get('crash_type')}`
- Mapped location: `{report.get('mapped_location')}`

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
""".strip()+"\n"
    path = output_dir / "PR_DESCRIPTION.md"
    path.write_text(md, encoding="utf-8")
    return str(path)
