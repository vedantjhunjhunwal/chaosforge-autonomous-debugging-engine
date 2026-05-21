# ChaosForge Production Architecture

This project keeps the debugging loop focused and productized:

1. Adversary generates payloads.
2. Fuzzing Sandbox executes payloads against a universal target contract.
3. Crash Check classifies failures.
4. Code Surgeon maps failures to source and generates patch artifacts.
5. Monte Carlo CI runs regression commands repeatedly.
6. Final Compiler writes report and PR artifact.

The system is language-agnostic because every target is treated as an executable boundary.
