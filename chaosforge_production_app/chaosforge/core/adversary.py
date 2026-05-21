import json, random

def generate_payloads(round_id: int = 1) -> list[dict]:
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
    return base

def payload_to_arg(payload: dict) -> str:
    return json.dumps(payload, separators=(",", ":"))
