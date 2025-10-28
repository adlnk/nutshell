# nutshell

Command-line tool for summarizing research papers using Claude API.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Usage

Basic usage:

```bash
python nutshell.py paper.pdf
```

This will create `paper_summary.md` in the same directory as the PDF.

Specify output location:

```bash
python nutshell.py paper.pdf -o output/summary.md
```

Use a different model:

```bash
python nutshell.py paper.pdf -m claude-3-5-sonnet-20241022
```

## How it works

1. Loads the PDF file
2. Sends it to Claude API with a summarization prompt
3. Saves the generated summary as a markdown file

The summary captures key findings, methodology, results, and other salient points while being more concise than the original paper.
