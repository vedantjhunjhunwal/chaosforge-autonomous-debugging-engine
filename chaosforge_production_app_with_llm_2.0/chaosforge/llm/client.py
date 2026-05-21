import json
import re
from typing import Any
import requests
from chaosforge import config

class LLMClient:
    """Small provider-agnostic LLM client.

    Uses direct HTTP calls to avoid forcing heavyweight SDK installs.
    Supported providers:
      - openai / openai-compatible: POST /chat/completions
      - gemini: Gemini generateContent REST API
    """
    def __init__(self):
        self.mode = config.LLM_MODE
        self.provider = config.LLM_PROVIDER
        self.model = config.LLM_MODEL
        self.last_error = ""

    @property
    def enabled(self) -> bool:
        if self.mode == "off" or self.provider in {"", "off", "none"}:
            return False
        if self.provider in {"openai", "openai-compatible"}:
            return bool(config.OPENAI_API_KEY)
        if self.provider == "gemini":
            return bool(config.GOOGLE_API_KEY)
        return False

    def complete(self, system: str, prompt: str, temperature: float = 0.2) -> str | None:
        if not self.enabled:
            self.last_error = "LLM disabled or API key missing"
            if self.mode == "strict":
                raise RuntimeError(self.last_error)
            return None
        try:
            if self.provider in {"openai", "openai-compatible"}:
                return self._openai_chat(system, prompt, temperature)
            if self.provider == "gemini":
                return self._gemini(system, prompt, temperature)
            self.last_error = f"unsupported provider: {self.provider}"
            return None
        except Exception as exc:
            self.last_error = repr(exc)
            if self.mode == "strict":
                raise
            return None

    def _openai_chat(self, system: str, prompt: str, temperature: float) -> str:
        url = config.OPENAI_BASE_URL.rstrip("/") + "/chat/completions"
        headers = {
            "Authorization": f"Bearer {config.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        }
        r = requests.post(url, headers=headers, json=payload, timeout=config.LLM_REQUEST_TIMEOUT)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    def _gemini(self, system: str, prompt: str, temperature: float) -> str:
        model = config.GEMINI_MODEL or self.model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={config.GOOGLE_API_KEY}"
        payload = {
            "generationConfig": {"temperature": temperature},
            "contents": [{"parts": [{"text": system + "\n\n" + prompt}]}],
        }
        r = requests.post(url, json=payload, timeout=config.LLM_REQUEST_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]


def extract_json(text: str) -> Any | None:
    if not text:
        return None
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except Exception:
        pass
    # Try to find first JSON object/array in the response.
    for start, end in [("[", "]"), ("{", "}")]:
        i = cleaned.find(start)
        j = cleaned.rfind(end)
        if i != -1 and j != -1 and j > i:
            try:
                return json.loads(cleaned[i:j+1])
            except Exception:
                continue
    return None
