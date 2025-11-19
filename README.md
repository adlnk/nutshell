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

### Transcribe a paper

Create a full text transcription with figures converted to descriptions:

```bash
nutshell transcribe paper.pdf
```

This will create `paper_transcription.md` with:
- Complete verbatim text from the paper
- Figures and images converted to detailed text descriptions
- Tables converted to markdown format
- An HTML comment at the top noting it's an AI-generated transcript

All the same options as summarize are available:

```bash
nutshell transcribe paper.pdf -o output/transcript.md
nutshell transcribe paper.pdf -m claude-3-5-haiku-20241022
nutshell transcribe paper.pdf -p your_transcribe_prompt.txt
```

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
