import uuid, json, shutil
from pathlib import Path
from sqlalchemy.orm import Session
from chaosforge.schemas import TargetContract
from chaosforge.db.models import Run
from chaosforge.core.artifacts import make_run_dir, write_json, write_text
from chaosforge.core.scanner import scan_repository
from chaosforge.core.parser import parse_sources
from chaosforge.core.adversary import generate_payloads
from chaosforge.core.sandbox import run_build, execute_payload, run_shell, render_command
from chaosforge.core.crash_mapper import map_crash
from chaosforge.core.patcher import generate_patch
from chaosforge.core.testgen import generate_regression_test
from chaosforge.core.ci_runner import run_monte_carlo
from chaosforge.core.pr import write_pr_artifact

class ChaosForgeEngine:
    def __init__(self, db: Session | None = None):
        self.db = db

    def create_run(self, contract: TargetContract, user_id: int | None = None) -> Run:
        run_id = uuid.uuid4().hex[:12]
        artifact_dir = make_run_dir(run_id)
        run = Run(id=run_id, user_id=user_id, target_name=contract.name, status="queued", contract_json=contract.model_dump_json(indent=2), artifact_dir=str(artifact_dir))
        if self.db:
            self.db.add(run); self.db.commit(); self.db.refresh(run)
        return run

    def execute_run(self, run_id: str, contract: TargetContract, runs: int = 100, concurrency: int = 8) -> dict:
        output_dir = make_run_dir(run_id)
        final = {"id": run_id, "target_name": contract.name, "status": "running", "artifact_dir": str(output_dir)}
        self._update(run_id, status="running")
        try:
            write_text(output_dir / "contract.json", contract.model_dump_json(indent=2))
            scan = scan_repository(contract.workdir, contract.source_files)
            write_json(output_dir / "repository_scan.json", scan)
            parsed = parse_sources(contract.source_files, contract.workdir)
            write_json(output_dir / "source_symbols.json", parsed)
            build = run_build(contract)
            if build:
                write_json(output_dir / "build_result.json", build.to_dict())
                if build.exit_code != 0:
                    raise RuntimeError("build failed: " + build.stderr[-500:])

            crash = None
            payloads = []
            for round_id in range(1, 4):
                batch = generate_payloads(round_id)
                payloads.extend(batch)
                for payload in batch:
                    result = execute_payload(contract, payload)
                    if result.crashed:
                        crash = (payload, result)
                        break
                if crash:
                    break
            write_json(output_dir / "payloads.json", payloads)

            if not crash:
                final.update({"status":"no_crash_found", "crash_found":False, "ci_passes":0, "ci_total":0})
                write_json(output_dir / "final_report.json", final)
                write_pr_artifact(output_dir, final)
                self._update(run_id, status="no_crash_found", crash_found=False)
                return final

            payload, result = crash
            write_json(output_dir / "failing_payload.json", payload)
            write_json(output_dir / "crash_result.json", result.to_dict())
            write_text(output_dir / "crash_trace.txt", result.stderr or result.stdout)
            mapped = map_crash(result.to_dict(), contract.source_files, contract.workdir)
            mapped_location = f"{mapped.get('file')}:{mapped.get('line')}"
            write_json(output_dir / "crash_mapping.json", mapped)

            # Try patch loop. Current engine creates patch artifacts; if project has test command, it runs it.
            patch = generate_patch(mapped.get("file") or (contract.source_files[0] if contract.source_files else ""), result.crash_type, int(mapped.get("line") or 1), output_dir)
            write_json(output_dir / "patch_summary.json", {k:v for k,v in patch.items() if k != "diff"})
            test = generate_regression_test(contract, payload, output_dir)
            write_json(output_dir / "generated_test.json", test)

            # Use native test command if available; otherwise use generated regression shell.
            test_cmd = contract.test_command if contract.test_command else str(Path(test["test_path"]).resolve())
            ci = run_monte_carlo(test_cmd, contract.workdir, runs, concurrency, contract.timeout_seconds)
            write_json(output_dir / "monte_carlo_report.json", ci)

            status = "completed" if ci["stable"] else "ci_failed"
            final.update({
                "status": status,
                "crash_found": True,
                "crash_type": result.crash_type,
                "mapped_location": mapped_location,
                "ci_passes": ci["passes"],
                "ci_total": ci["total"],
                "patch_generated": bool(patch.get("patched")),
            })
            write_json(output_dir / "final_report.json", final)
            write_pr_artifact(output_dir, final)
            self._update(run_id, status=status, crash_found=True, crash_type=result.crash_type, mapped_location=mapped_location, ci_passes=ci["passes"], ci_total=ci["total"])
            return final
        except Exception as e:
            final.update({"status":"failed", "error":repr(e)})
            write_json(output_dir / "final_report.json", final)
            self._update(run_id, status="failed", error=repr(e))
            return final

    def _update(self, run_id: str, **fields):
        if not self.db: return
        run = self.db.get(Run, run_id)
        if not run: return
        for k,v in fields.items(): setattr(run, k, v)
        self.db.commit()
