def calculate_margin(payload):
    amount = payload.get("amount", 100)
    price = payload.get("price", 1)
    return amount / price
