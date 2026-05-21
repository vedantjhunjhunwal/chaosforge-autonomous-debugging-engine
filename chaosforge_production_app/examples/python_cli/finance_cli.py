import json, sys
from finance import calculate_margin

if __name__ == "__main__":
    payload = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    print(calculate_margin(payload))
