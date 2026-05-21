import json
from chaosforge.llm.client import extract_json


def generate_payloads(round_id: int = 1, contract=None, scan: dict | None = None, llm=None) -> list[dict]:
    """Node 1: The Adversary.

    If an LLM key is configured, ChaosForge asks the LLM for target-aware payloads.
    If not, it uses deterministic fallback payloads so the product still works locally.
    """
    if llm and getattr(llm, "enabled", False):
        generated = _llm_payloads(round_id, contract, scan, llm)
        if generated:
            return generated
    return deterministic_payloads(round_id)


def _llm_payloads(round_id: int, contract, scan: dict | None, llm) -> list[dict] | None:
    system = """You are ChaosForge Adversary Agent, an expert software fuzzer.
Generate destructive but safe JSON payloads for local testing only.
Return ONLY a JSON array of exactly 10 objects. No markdown."""
    prompt = {
        "round_id": round_id,
        "target_contract": contract.model_dump() if contract else {},
        "repository_scan_sample": (scan or {}).get("files", [])[:20],
        "instructions": [
            "Generate edge cases likely to crash parsers, financial calculations, APIs, CLIs, and compiled binaries.",
            "Include divide-by-zero, nulls, missing keys, huge numbers, nested arrays, strings where numbers are expected, unicode, empty values, and boundary values.",
            "Each payload must include a short unique id field.",
        ],
    }
    text = llm.complete(system, json.dumps(prompt, indent=2), temperature=0.4)
    data = extract_json(text or "")
    if isinstance(data, list):
        out = [p for p in data if isinstance(p, dict)]
        if out:
            for i, p in enumerate(out[:10], 1):
                p.setdefault("id", f"llm_round_{round_id}_{i}")
                p["round"] = round_id
                p["generated_by"] = "llm"
            return out[:10]
    return None


def deterministic_payloads(round_id: int = 1) -> list[dict]:
    base = [
        {"id":"zero_division", "amount":100, "price":0, "volume":10, "values":[1,2,3]},
        {"id":"negative_price", "amount":100, "price":-1, "volume":10, "values":[-1,-2]},
        {"id":"empty_values", "amount":100, "price":5, "volume":0, "values":[]},
        {"id":"huge_int", "amount":10**18, "price":1, "volume":10**12, "values":[10**18]},
        {"id":"tiny_float", "amount":1e-18, "price":1e-18, "volume":1, "values":[1e-18]},
        {"id":"none_fields", "amount":None, "price":0, "volume":None, "values":None},
        {"id":"string_fields", "amount":"100", "price":"0", "volume":"bad", "values":"oops"},
        {"id":"nested_arrays", "amount":10, "price":0, "volume":1, "values":[[[]]]},
        {"id":"nan_like", "amount":"NaN", "price":0, "volume":"Infinity", "values":["NaN"]},
        {"id":"missing_fields"},
    ]
    for p in base:
        p["round"] = round_id
        p["generated_by"] = "deterministic"
    return base


def payload_to_arg(payload: dict) -> str:
    return json.dumps(payload, separators=(",", ":"))
