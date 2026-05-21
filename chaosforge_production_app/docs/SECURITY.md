# Security Notes

ChaosForge executes user-provided commands. For local demos this is acceptable, but for hosted production use:

- Run jobs inside isolated containers.
- Drop Linux capabilities.
- Use read-only mounts.
- Enforce CPU/memory/network limits.
- Store secrets outside artifacts.
- Use a job queue and worker pool.
- Audit all command contracts before execution.
