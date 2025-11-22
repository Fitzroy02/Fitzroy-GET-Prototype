import json
import os

def load_json(path: str) -> dict:
    """
    Load JSON data from a file.
    Returns an empty dict if the file does not exist or is invalid.
    """
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_json(path: str, data: dict) -> None:
    """
    Save JSON data to a file.
    Creates the file if it does not exist.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
