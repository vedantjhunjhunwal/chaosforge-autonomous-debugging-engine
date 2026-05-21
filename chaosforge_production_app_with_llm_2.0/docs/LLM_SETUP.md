# LLM Setup for ChaosForge

ChaosForge works without an LLM. In that case it uses deterministic fallback agents.
To make it LLM-powered, create a `.env` file in the project root.

## OpenAI

```env
LLM_MODE=auto
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=your_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
```

## Gemini

```env
LLM_MODE=auto
LLM_PROVIDER=gemini
GEMINI_MODEL=gemini-1.5-flash
GOOGLE_API_KEY=your_key_here
```

## What becomes LLM-powered?

- Node 1: Adversary Agent generates target-aware adversarial payloads.
- Node 3: Code Surgeon Agent reads crash trace and source code, then proposes patched full-file code.
- Node 5: Final Compiler Agent writes a PR-style Markdown report.

If an API key is missing or the LLM call fails, `LLM_MODE=auto` safely falls back to deterministic logic.
Use `LLM_MODE=strict` only when you want the run to fail if the LLM is unavailable.
