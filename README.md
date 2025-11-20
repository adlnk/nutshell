# nutshell

Command-line tool for summarizing and transcribing research papers using Claude API.

## Installation

Install the package:

```bash
pip install -e .
```

Or for development:

```bash
git clone <repository>
cd "Research Bot"
pip install -e .
```

Set your Anthropic API key (choose one method):

**Option 1: Config file (recommended)**
```bash
mkdir -p ~/.config/nutshell
echo "ANTHROPIC_API_KEY=your-api-key-here" > ~/.config/nutshell/config
```

**Option 2: Environment variable**
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

The config file method is preferred because:
- Available system-wide in all terminal sessions
- Not stored in dotfiles that might be version controlled
- Follows XDG Base Directory specification

## Usage

### Summarize a paper

Basic usage (local file or URL):

```bash
nutshell summarize paper.pdf
nutshell summarize https://arxiv.org/pdf/2402.02896
```

This will create a summary in the current directory (e.g., `paper_summary.md` or `2402.02896_summary.md` for arXiv papers).

**Model shortcuts:**
```bash
nutshell summarize paper.pdf -m haiku        # Fast and cheap (default for testing)
nutshell summarize paper.pdf -m sonnet       # Better quality (default)
nutshell summarize paper.pdf -m opus         # Highest quality (expensive, shows warning)
nutshell summarize paper.pdf -m haiku-latest # Use latest Haiku version
```

Available shortcuts: `haiku`, `sonnet`, `opus`, `haiku-3.5`, `sonnet-4.5`, `opus-3`, `haiku-latest`, `sonnet-latest`, `opus-latest`

You can also use full model IDs like `claude-3-5-haiku-20241022`.

**Other options:**
```bash
nutshell summarize paper.pdf -o output/summary.md  # Custom output path
nutshell summarize paper.pdf -p v1_baseline.txt    # Different prompt variant
```

**URL support:**
- PDFs are downloaded and cached in `~/.cache/nutshell/pdfs/`
- Re-using the same URL will use the cached version (no re-download)
- arXiv URLs automatically extract paper ID for output filename

### Transcribe a paper

Create a full text transcription with figures converted to descriptions:

```bash
nutshell transcribe paper.pdf
nutshell transcribe https://arxiv.org/pdf/2402.02896
```

This will create a transcription (e.g., `paper_transcription.md`) with:
- Complete verbatim text from the paper
- Figures and images converted to detailed text descriptions
- Tables converted to markdown format
- An HTML comment at the top noting it's an AI-generated transcript

All the same options as summarize are available (model shortcuts, URLs, custom output, etc.)

### Available commands

```bash
nutshell --help                # Show all commands
nutshell summarize --help      # Show summarize options
nutshell transcribe --help     # Show transcribe options
```

## How it works

### Summarize
1. Loads the PDF file
2. Sends it to Claude API with a summarization prompt (uses Sonnet 4.5 by default)
3. Saves the generated summary as a markdown file

The summary captures key findings, methodology, results, and other salient points while being more concise than the original paper.

### Transcribe
1. Loads the PDF file
2. Sends it to Claude API with a transcription prompt (uses Sonnet 4.5 by default, 16K token limit)
3. Converts all visual elements to text descriptions
4. Adds a disclaimer comment at the top
5. Saves the complete transcription as a markdown file

The transcription preserves all textual content verbatim and converts figures/tables to text format, optimizing the paper for use as context in AI conversations.

## Development

### Project structure

- `nutshell_pkg/` - Main package code
  - `cli.py` - Command-line interface with subcommands
  - `core.py` - Core summarization functionality
- `Prompts/` - Versioned prompt templates
- `setup.py` - Package installation configuration

### Running tests

```bash
# Test summarization
nutshell summarize sample_paper.pdf

# Test transcription
nutshell transcribe sample_paper.pdf
```

### Adding new prompts

Create a new prompt file in `Prompts/` directory and document it in `Prompts/changelog.txt`. Use it with:

```bash
nutshell summarize paper.pdf -p your_new_prompt.txt
```
