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


def create_summary_prompt():
    """Return the base prompt for paper summarization."""
    return """You will create a comprehensive reference document for a scientific or technical paper that can be used by research-focused AI agents and researchers. This reference document should capture all salient points while being much more concise than the original paper.

Your task is to create a reference document that serves three main purposes:

1. **Reference for AI assistants**: Can be included in conversation context when discussing relevant topics
2. **Research summary**: Helps researchers avoid reading the entire paper when time is limited
3. **Comprehensive reference**: Covers at least 95% of cases where someone would need to reference or think about this paper later

## Content Prioritization Guidelines

Focus on:

- Key findings and conclusions
- Methodology and experimental design
- Important results and data
- Limitations and future work
- Novel concepts or frameworks introduced
- Specific quotations that might be worth citing in future research
- Technical details that would be important for replication or further research

## Formatting Requirements

- Reference all information to specific sections, page numbers, figures, or tables from the original paper
- Include direct quotations for particularly important passages, properly attributed
- Use clear headings and subheadings to organize content
- Maintain enough detail to be genuinely useful while being significantly more concise than the original
- When in doubt about level of detail, err on the side of including more rather than less

## Process

First, use a scratchpad to plan your approach:

<scratchpad>
- Identify the main sections and themes of the paper
- Note which parts are most relevant
- Plan the structure of your reference document
- Identify key quotations and technical details to preserve
</scratchpad>

Then create your reference document. Structure it logically with clear headings, and ensure that every major point includes proper attribution to the source location in the original paper.

Your final output should be a well-organized reference document that captures the essential content of the paper in a format optimized for future reference and research use."""


def summarize_paper(pdf_path, model="claude-sonnet-4-5-20250929"):
    """
    Send PDF to Claude API and get summary.

    Args:
        pdf_path: Path to PDF file
        model: Claude model to use

    Returns:
        Summary text as string
    """
    client = Anthropic()

    pdf_data = load_pdf(pdf_path)
    pdf_base64 = base64.standard_b64encode(pdf_data).decode('utf-8')
    prompt = create_summary_prompt()

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

    try:
        summary = summarize_paper(pdf_path, model=args.model)
        save_summary(summary, output_path)
        print(f"✓ Summary saved to: {output_path}")
    except Exception as e:
        print(f"\033[31m✗ Summarization failed:\033[0m {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
