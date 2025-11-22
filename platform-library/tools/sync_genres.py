#!/usr/bin/env python3
"""
sync_genres.py
Validates the filesystem against config/genres.json and creates missing folders automatically.
"""

import os
import json
import argparse

# Path to your config file
CONFIG_PATH = "platform-library/config/genres.json"
BASE_DIR = "platform-library"

def load_genres():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found at {CONFIG_PATH}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        exit(1)

def safe_name(name):
    """Convert genre/subgenre names into lowercase, underscore-safe folder names."""
    return name.lower().replace(" ", "_").replace("&", "and")

def ensure_folder(path, dry_run=False, verbose=False):
    """Create folder if it doesn't exist."""
    if not os.path.exists(path):
        if dry_run:
            print(f"[DRY RUN] Would create: {path}")
        else:
            os.makedirs(path)
            print(f"Created: {path}")
    else:
        if verbose:
            print(f"Exists: {path}")

def sync_structure(dry_run=False, verbose=False):
    data = load_genres()
    for genre in data["genres"]:
        genre_folder = os.path.join(BASE_DIR, safe_name(genre["name"]))
        ensure_folder(genre_folder, dry_run, verbose)

        for sub in genre.get("subgenres", []):
            sub_folder = os.path.join(genre_folder, safe_name(sub))
            ensure_folder(sub_folder, dry_run, verbose)

    # Handle cross-tags separately
    cross_folder = os.path.join(BASE_DIR, "cross_tags")
    ensure_folder(cross_folder, dry_run, verbose)
    for tag in data.get("crossTags", []):
        tag_folder = os.path.join(cross_folder, safe_name(tag["name"]))
        ensure_folder(tag_folder, dry_run, verbose)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync platform-library structure with genres.json")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without creating folders")
    parser.add_argument("--verbose", action="store_true", help="Show all folders including existing ones")
    args = parser.parse_args()
    
    sync_structure(dry_run=args.dry_run, verbose=args.verbose)