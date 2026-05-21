from concurrent.futures import ThreadPoolExecutor, as_completed
from chaosforge.core.sandbox import run_shell

def run_monte_carlo(test_command: str, workdir: str, total_runs: int, concurrency: int, timeout: int) -> dict:
    results=[]
    passes=0
    with ThreadPoolExecutor(max_workers=max(1, concurrency)) as ex:
        futs=[ex.submit(run_shell, test_command, workdir, timeout, f"ci_{i}") for i in range(total_runs)]
        for i, fut in enumerate(as_completed(futs), 1):
            r=fut.result()
            ok = r.exit_code == 0 and not r.timed_out
            passes += 1 if ok else 0
            results.append(r.to_dict() | {"ok": ok})
    return {"passes": passes, "total": total_runs, "stable": passes == total_runs, "results": results[:50]}
