# EPUB Translation Skills

An AI-agent-agnostic project for translating EPUB files, following the [Agent Skills](https://agentskills.io/) format. Works with **Gemini CLI**, **Claude Code**, and other compliant agents.

## Installation

### 🌐 Universal (Cursor, Windsurf, Aider, etc.)
Install via the [skills](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills add mauriciopoppe/epub-translation
```

### Gemini CLI
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

## Usage

Once installed, your agent will have the expertise to handle EPUB translation tasks surgically.

### Example: Translating a Book
Simply ask your agent to perform the translation. It will use the skill's scripts to deconstruct the EPUB, translate the content while preserving formatting, and reconstruct the final file.

**Prompt:**
> Translate `my-book.epub` from English to French.

**What the agent does:**
1.  **Extracts** the EPUB structure into a temporary workspace.
2.  **Surgically translates** text nodes in all XHTML files (preserving HTML tags and attributes).
3.  **Updates metadata** to reflect the new language (`fr`).
4.  **Re-packs** the EPUB following the strict `mimetype` specification.

## Token Usage

Translating a book involves both the content payload and the agent's internal overhead (instructions and system prompts).

### Estimate for a 1,000-Word Book
For a 1,000-word book being translated from English to French:

| Component | Input Tokens | Output Tokens |
| :--- | :--- | :--- |
| Agent & Skill Overhead | ~2,000 | - |
| Book Content (English + HTML) | ~1,500 | - |
| Translation (French) | - | ~1,800 |
| **Total** | **~3,500** | **~1,800** |

**Total Estimated cost:** ~5,300 tokens per 1,000 words.

*Note: If the book is split into multiple chapters, the overhead is sent per chapter. A 10,000-word book split into 10 chapters will consume more tokens than the same book processed in fewer chunks.*

## Features
- **Structural Integrity:** Preserves EPUB spec requirements (mimetype rule).
- **Format Preservation:** Surgically replaces text nodes while keeping HTML attributes intact.
- **Metadata Management:** Automatically updates book language tags.

## License
MIT
