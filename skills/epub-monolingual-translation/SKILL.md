---
name: epub-monolingual-translation
description: Convert monolingual EPUB files from a source language to a target language. Use when asked to translate an EPUB, ebook, or book file while preserving its technical integrity, structural layout, and metadata.
---

# EPUB Monolingual Translation Skill

## Overview
This skill enables agents to translate EPUB files. It handles deconstruction, surgical text replacement (preserving HTML attributes), metadata updates, and spec-compliant reconstruction.

## Location
Supporting scripts are located in the `scripts/` directory **adjacent to this `SKILL.md`**.

## Dependencies
- Python 3.x
- `beautifulsoup4`, `lxml`
- Environment: Use the project's `.venv` if available, or create one: `python3 -m venv .venv`

## Workflow

### 1. Setup
Ensure the virtual environment is ready and dependencies are installed.
- **Mac/Linux:** `source .venv/bin/activate && pip install beautifulsoup4 lxml`
- **Windows:** `.venv\Scripts\activate && pip install beautifulsoup4 lxml`

### 2. Deconstruction
Extract the EPUB to a temporary directory.
```bash
python3 ./scripts/epub_manager.py extract <INPUT_FILE> <TEMP_DIR>
```

### 3. Translation
Iterate through `.xhtml` or `.html` files in `<TEMP_DIR>`.
1. **Extract**: `ID:N|text` strings using `./scripts/translate_processor.py extract`.
2. **Translate**: Translate the text content to the target language. Preserve 'product manager'.
3. **Apply**: Save translations to a temp file and use `./scripts/translate_processor.py apply`.

### 4. Metadata
Update `<dc:language>` in `content.opf`.
```bash
python3 ./scripts/translate_processor.py metadata <OPF_FILE> <LANG_CODE>
```

### 5. Reconstruction
Re-pack the EPUB. The script handles the `mimetype` rule.
```bash
python3 ./scripts/epub_manager.py pack <TEMP_DIR> <OUTPUT_FILE>
```

## Validation
To ensure the scripts are functioning correctly, you can run the included unit tests:
```bash
python3 -m unittest discover ./tests
```

## Guidelines
- Always use the `.venv` python interpreter.
- Maintain all HTML tags/attributes exactly.
- The `mimetype` file must be first and uncompressed (enforced by `epub_manager.py`).
