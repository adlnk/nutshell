# nutshell

Command-line tool for summarizing research papers using Claude API.

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

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Usage

### Summarize a paper

Basic usage:

```bash
nutshell summarize paper.pdf
```

This will create `paper_summary.md` in the same directory as the PDF.

Specify output location:

```bash
nutshell summarize paper.pdf -o output/summary.md
```

Use a different model:

```bash
nutshell summarize paper.pdf -m claude-3-5-haiku-20241022
```

Use a different prompt variant:

```bash
nutshell summarize paper.pdf -p v1_baseline.txt
```

### Available commands

```bash
nutshell --help                # Show all commands
nutshell summarize --help      # Show summarize options
```

## How it works

1. Loads the PDF file
2. Sends it to Claude API with a summarization prompt (uses Sonnet 4.5 by default)
3. Saves the generated summary as a markdown file

The summary captures key findings, methodology, results, and other salient points while being more concise than the original paper.

## Development

### Project structure

- `nutshell_pkg/` - Main package code
  - `cli.py` - Command-line interface with subcommands
  - `core.py` - Core summarization functionality
- `Prompts/` - Versioned prompt templates
- `setup.py` - Package installation configuration

### Running tests

```bash
# Test with a sample paper
nutshell summarize sample_paper.pdf
```

### Adding new prompts

Create a new prompt file in `Prompts/` directory and document it in `Prompts/changelog.txt`. Use it with:

```bash
nutshell summarize paper.pdf -p your_new_prompt.txt
```
