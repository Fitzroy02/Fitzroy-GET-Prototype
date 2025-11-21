#!/usr/bin/env python3
"""
sync_genres.py
Validates the filesystem against config/genres.json and creates missing folders automatically.
"""

import os
import json

# Path to your config file
CONFIG_PATH = "platform-library/config/genres.json"
BASE_DIR = "platform-library"

def load_genres():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def safe_name(name):
    """Convert genre/subgenre names into lowercase, underscore-safe folder names."""
    return name.lower().replace(" ", "_").replace("&", "and")

def ensure_folder(path):
    """Create folder if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created: {path}")
    else:
        print(f"Exists: {path}")

def sync_structure():
    data = load_genres()
    for genre in data["genres"]:
        genre_folder = os.path.join(BASE_DIR, safe_name(genre["name"]))
        ensure_folder(genre_folder)

        for sub in genre.get("subgenres", []):
            sub_folder = os.path.join(genre_folder, safe_name(sub))
            ensure_folder(sub_folder)

    # Handle cross-tags separately
    cross_folder = os.path.join(BASE_DIR, "cross_tags")
    ensure_folder(cross_folder)
    for tag in data.get("crossTags", []):
        tag_folder = os.path.join(cross_folder, safe_name(tag["name"]))
        ensure_folder(tag_folder)

if __name__ == "__main__":
    sync_structure()