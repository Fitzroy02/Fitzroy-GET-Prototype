# Platform Library

This directory contains the platform-library scaffold for organizing media content by genre.

## Structure

The platform library uses a hierarchical structure based on genres and subgenres defined in `config/genres.json`.

### Configuration

- **config/genres.json**: Defines the genre taxonomy including main genres, subgenres, and cross-tags

### Tools

- **tools/sync_genres.py**: Python script to synchronize the filesystem with the genre schema
  - Validates the filesystem against config/genres.json
  - Creates missing folders automatically
  - Can be run in dry-run mode for preview

## Usage

### Preview Changes (Dry Run)

```bash
python3 platform-library/tools/sync_genres.py --dry-run --verbose
```

### Apply Changes

```bash
python3 platform-library/tools/sync_genres.py
```

## Validation

The `.github/workflows/sync-genres.yml` workflow automatically validates the structure on pull requests and pushes.

## Directory Structure

The script generates folders based on the genre schema:

```
platform-library/
├── config/
│   └── genres.json
├── tools/
│   └── sync_genres.py
├── fiction/
│   ├── science_fiction/
│   ├── fantasy/
│   └── ...
├── non-fiction/
│   ├── biography/
│   ├── memoir/
│   └── ...
├── poetry/
│   └── ...
└── cross_tags/
    ├── coming_of_age/
    ├── dystopian/
    └── ...
```

## Notes

- Folder names are automatically converted to lowercase with underscores
- The `uploads/` directory can optionally be added to `.gitignore`
- README placeholders can be added to genre folders for documentation
