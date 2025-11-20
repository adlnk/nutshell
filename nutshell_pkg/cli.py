"""
Command-line interface for nutshell
"""

import argparse
import sys
from pathlib import Path
from nutshell_pkg.core import (
    summarize_paper, save_summary, transcribe_paper, save_transcription, calculate_cost,
    resolve_model_name, download_pdf_from_url, extract_arxiv_id
)


def check_opus_warning(model_name):
    """
    Check if model is opus and show warning.

    Args:
        model_name: Model name (resolved or shortcut)

    Returns:
        True if user confirms, False otherwise
    """
    if 'opus' in model_name.lower():
        print("\n\033[33m⚠ Warning: Opus models are very expensive and may not provide")
        print("significant benefits for summarization/transcription tasks.")
        print("Consider using 'sonnet' or 'haiku' instead.\033[0m\n")
        response = input("Continue with opus? (y/N): ").strip().lower()
        return response == 'y'
    return True


def resolve_pdf_path(pdf_input):
    """
    Resolve PDF input (URL or file path) to a local file path.

    Args:
        pdf_input: URL or file path string

    Returns:
        Tuple of (Path object, suggested output name)
    """
    # Check if it's a URL
    if pdf_input.startswith('http://') or pdf_input.startswith('https://'):
        # Download and cache PDF
        cached_path = download_pdf_from_url(pdf_input)

        # Try to extract arXiv ID for output naming
        arxiv_id = extract_arxiv_id(pdf_input)
        suggested_name = arxiv_id if arxiv_id else Path(cached_path).stem

        return cached_path, suggested_name
    else:
        # It's a file path
        pdf_path = Path(pdf_input)
        return pdf_path, pdf_path.stem


def cmd_summarize(args):
    """Handle the summarize subcommand."""
    # Resolve model shortname
    model = resolve_model_name(args.model)

    # Check for opus warning
    if not check_opus_warning(model):
        print("Aborted.")
        sys.exit(0)

    # Resolve PDF input (URL or file path)
    try:
        pdf_path, suggested_name = resolve_pdf_path(args.pdf_path)
    except Exception as e:
        print(f"\033[31m✗ Error:\033[0m {e}")
        sys.exit(1)

    # Validate file exists (for local paths)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        # Use current directory with suggested name
        output_path = Path.cwd() / f"{suggested_name}_summary.md"

    print(f"Processing: {pdf_path}")
    print(f"Using model: {model}")
    print(f"Using prompt: {args.prompt}")

    try:
        summary, usage = summarize_paper(pdf_path, model=model, prompt_file=args.prompt)
        save_summary(summary, output_path)
        print(f"✓ Summary saved to: {output_path}")

        # Print usage stats
        print(f"\nTokens: {usage.input_tokens:,} in, {usage.output_tokens:,} out")
        cost = calculate_cost(model, usage.input_tokens, usage.output_tokens)
        if cost is not None:
            print(f"Cost: ${cost:.4f}")
    except Exception as e:
        print(f"\033[31m✗ Summarization failed:\033[0m {e}")
        sys.exit(1)


def cmd_transcribe(args):
    """Handle the transcribe subcommand."""
    # Resolve model shortname
    model = resolve_model_name(args.model)

    # Check for opus warning
    if not check_opus_warning(model):
        print("Aborted.")
        sys.exit(0)

    # Resolve PDF input (URL or file path)
    try:
        pdf_path, suggested_name = resolve_pdf_path(args.pdf_path)
    except Exception as e:
        print(f"\033[31m✗ Error:\033[0m {e}")
        sys.exit(1)

    # Validate file exists (for local paths)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        # Use current directory with suggested name
        output_path = Path.cwd() / f"{suggested_name}_transcription.md"

    print(f"Processing: {pdf_path}")
    print(f"Using model: {model}")
    print(f"Using prompt: {args.prompt}")

    try:
        transcription, usage = transcribe_paper(pdf_path, model=model, prompt_file=args.prompt)
        save_transcription(transcription, output_path)
        print(f"✓ Transcription saved to: {output_path}")

        # Print usage stats
        print(f"\nTokens: {usage.input_tokens:,} in, {usage.output_tokens:,} out")
        cost = calculate_cost(model, usage.input_tokens, usage.output_tokens)
        if cost is not None:
            print(f"Cost: ${cost:.4f}")
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
        help='Path or URL to PDF file to summarize'
    )
    summarize_parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output path for summary (default: <pdf_name>_summary.md)'
    )
    summarize_parser.add_argument(
        '-m', '--model',
        type=str,
        default='sonnet',
        help='Model to use: sonnet (default), haiku, opus, or full model ID'
    )
    summarize_parser.add_argument(
        '-p', '--prompt',
        type=str,
        default='v2_no_scratchpad.txt',
        help='Prompt file to use from Prompts/ (default: v2_no_scratchpad.txt)'
    )
    summarize_parser.set_defaults(func=cmd_summarize)

    # Summarise subcommand (British spelling alias)
    summarise_parser = subparsers.add_parser(
        'summarise',
        help='Summarize a research paper (British spelling)'
    )
    summarise_parser.add_argument(
        'pdf_path',
        type=str,
        help='Path or URL to PDF file to summarize'
    )
    summarise_parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output path for summary (default: <pdf_name>_summary.md)'
    )
    summarise_parser.add_argument(
        '-m', '--model',
        type=str,
        default='sonnet',
        help='Model to use: sonnet (default), haiku, opus, or full model ID'
    )
    summarise_parser.add_argument(
        '-p', '--prompt',
        type=str,
        default='v2_no_scratchpad.txt',
        help='Prompt file to use from Prompts/ (default: v2_no_scratchpad.txt)'
    )
    summarise_parser.set_defaults(func=cmd_summarize)

    # Transcribe subcommand
    transcribe_parser = subparsers.add_parser(
        'transcribe',
        help='Create a full transcription of a research paper'
    )
    transcribe_parser.add_argument(
        'pdf_path',
        type=str,
        help='Path or URL to PDF file to transcribe'
    )
    transcribe_parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output path for transcription (default: <pdf_name>_transcription.md)'
    )
    transcribe_parser.add_argument(
        '-m', '--model',
        type=str,
        default='sonnet',
        help='Model to use: sonnet (default), haiku, opus, or full model ID'
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
