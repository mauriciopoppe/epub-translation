# EPUB Translation Skills

An AI-agent-agnostic project for translating EPUB files, following the [Agent Skills](https://agentskills.io/) format. Works with **Gemini CLI**, **Claude Code**, and other compliant agents.

## Project Structure
- `skills/epub-monolingual-translation/`: The skill definition and supporting scripts.
  - `SKILL.md`: Metadata and instructions for the agent.
  - `scripts/`: Python utilities for EPUB manipulation.

## Installation

### Gemini CLI
Install the skill directly from the repository using the native command:

```bash
gemini skills install https://github.com/mauriciopoppe/epub-translation --path skills/epub-monolingual-translation
```

### Claude Code
Register the plugin marketplace and install the skill:

```
/plugin marketplace add mauriciopoppe/epub-translation
/plugin install epub-translation@epub-translation
```

The skill is then available as `/epub-translation:epub-monolingual-translation`.

### Manual Usage (Python Only)
If you want to run the scripts directly without an agent:

```bash
# Setup environment
python3 -m venv .venv
source .venv/bin/activate
pip install beautifulsoup4 lxml

# Example usage
./.venv/bin/python3 skills/epub-monolingual-translation/scripts/epub_manager.py extract input.epub ./temp
```

## Features
- **Structural Integrity:** Preserves EPUB spec requirements (mimetype rule).
- **Format Preservation:** Surgically replaces text nodes while keeping HTML attributes intact.
- **Metadata Management:** Automatically updates book language tags.

## License
MIT
