"""
Command-line interface for nutshell
"""

import argparse
import sys
from pathlib import Path
from nutshell_pkg.core import summarize_paper, save_summary, transcribe_paper, save_transcription


def cmd_summarize(args):
    """Handle the summarize subcommand."""
    pdf_path = Path(args.pdf_path)

    # Validate input file exists
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


def cmd_transcribe(args):
    """Handle the transcribe subcommand."""
    pdf_path = Path(args.pdf_path)

    # Validate input file exists
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = pdf_path.parent / f"{pdf_path.stem}_transcription.md"

    print(f"Processing: {pdf_path}")
    print(f"Using model: {args.model}")
    print(f"Using prompt: {args.prompt}")

    try:
        transcription = transcribe_paper(pdf_path, model=args.model, prompt_file=args.prompt)
        save_transcription(transcription, output_path)
        print(f"✓ Transcription saved to: {output_path}")
    except Exception as e:
        print(f"\033[31m✗ Transcription failed:\033[0m {e}")
        sys.exit(1)


def main():
    """Main CLI entry point with subcommands."""
    parser = argparse.ArgumentParser(
        prog='nutshell',
        description='Research paper assistant tools using Claude API'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Summarize subcommand
    summarize_parser = subparsers.add_parser(
        'summarize',
        help='Summarize a research paper'
    )
    summarize_parser.add_argument(
        'pdf_path',
        type=str,
        help='Path to PDF file to summarize'
    )
    summarize_parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output path for summary (default: <pdf_name>_summary.md)'
    )
    summarize_parser.add_argument(
        '-m', '--model',
        type=str,
        default='claude-sonnet-4-5-20250929',
        help='Claude model to use (default: claude-sonnet-4-5-20250929)'
    )
    summarize_parser.add_argument(
        '-p', '--prompt',
        type=str,
        default='v2_no_scratchpad.txt',
        help='Prompt file to use from Prompts/ (default: v2_no_scratchpad.txt)'
    )
    summarize_parser.set_defaults(func=cmd_summarize)

    # Transcribe subcommand
    transcribe_parser = subparsers.add_parser(
        'transcribe',
        help='Create a full transcription of a research paper'
    )
    transcribe_parser.add_argument(
        'pdf_path',
        type=str,
        help='Path to PDF file to transcribe'
    )
    transcribe_parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output path for transcription (default: <pdf_name>_transcription.md)'
    )
    transcribe_parser.add_argument(
        '-m', '--model',
        type=str,
        default='claude-sonnet-4-5-20250929',
        help='Claude model to use (default: claude-sonnet-4-5-20250929)'
    )
    transcribe_parser.add_argument(
        '-p', '--prompt',
        type=str,
        default='transcribe_v1.txt',
        help='Prompt file to use from Prompts/ (default: transcribe_v1.txt)'
    )
    transcribe_parser.set_defaults(func=cmd_transcribe)

    args = parser.parse_args()

    # If no command specified, show help
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute the command
    args.func(args)


if __name__ == '__main__':
    main()
