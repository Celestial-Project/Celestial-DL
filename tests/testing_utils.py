import json

def load_json(filename: str) -> dict:
    with open(filename, encoding = 'utf-8') as f:
        return json.load(f)