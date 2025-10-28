#!/usr/bin/env python3
"""
nutshell: Command-line tool for summarizing research papers using Claude API
"""

import argparse
import base64
import sys
from pathlib import Path
from anthropic import Anthropic


def load_pdf(pdf_path):
    """Load PDF file and return file content."""
    with open(pdf_path, 'rb') as f:
        return f.read()


def load_prompt(prompt_file):
    """Load prompt from file."""
    script_dir = Path(__file__).parent
    prompt_path = script_dir / "Prompts" / prompt_file

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    with open(prompt_path, 'r') as f:
        return f.read()


def summarize_paper(pdf_path, model="claude-sonnet-4-5-20250929", prompt_file="v2_no_scratchpad.txt"):
    """
    Send PDF to Claude API and get summary.

    Args:
        pdf_path: Path to PDF file
        model: Claude model to use
        prompt_file: Prompt file to use from prompts/ directory

    Returns:
        Summary text as string
    """
    client = Anthropic()

    pdf_data = load_pdf(pdf_path)
    pdf_base64 = base64.standard_b64encode(pdf_data).decode('utf-8')
    prompt = load_prompt(prompt_file)

    # Use Claude's PDF analysis capability
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )

    return message.content[0].text


def save_summary(summary_text, output_path):
    """Save summary to markdown file."""
    with open(output_path, 'w') as f:
        f.write(summary_text)


def main():
    parser = argparse.ArgumentParser(
        description='Summarize research papers using Claude API'
    )
    parser.add_argument(
        'pdf_path',
        type=str,
        help='Path to PDF file to summarize'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output path for summary (default: <pdf_name>_summary.md)'
    )
    parser.add_argument(
        '-m', '--model',
        type=str,
        default='claude-sonnet-4-5-20250929',
        help='Claude model to use (default: claude-sonnet-4-5-20250929)'
    )
    parser.add_argument(
        '-p', '--prompt',
        type=str,
        default='v2_no_scratchpad.txt',
        help='Prompt file to use from Prompts/ (default: v2_no_scratchpad.txt)'
    )

    args = parser.parse_args()

    # Validate input file exists
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = pdf_path.parent / f"{pdf_path.stem}_summary.md"

    print(f"Processing: {pdf_path}")
    print(f"Using model: {args.model}")
    print(f"Using prompt: {args.prompt}")

    try:
        summary = summarize_paper(pdf_path, model=args.model, prompt_file=args.prompt)
        save_summary(summary, output_path)
        print(f"✓ Summary saved to: {output_path}")
    except Exception as e:
        print(f"\033[31m✗ Summarization failed:\033[0m {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
