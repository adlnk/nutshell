"""
Core functionality for paper summarization
"""

import base64
from pathlib import Path
from anthropic import Anthropic


def load_pdf(pdf_path):
    """Load PDF file and return file content."""
    with open(pdf_path, 'rb') as f:
        return f.read()


def load_prompt(prompt_file):
    """Load prompt from file."""
    # Look for Prompts directory relative to package installation
    pkg_dir = Path(__file__).parent.parent
    prompt_path = pkg_dir / "Prompts" / prompt_file

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
        prompt_file: Prompt file to use from Prompts/ directory

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


def transcribe_paper(pdf_path, model="claude-sonnet-4-5-20250929", prompt_file="transcribe_v1.txt"):
    """
    Send PDF to Claude API and get full transcription.

    Args:
        pdf_path: Path to PDF file
        model: Claude model to use
        prompt_file: Prompt file to use from Prompts/ directory

    Returns:
        Transcription text as string
    """
    client = Anthropic()

    pdf_data = load_pdf(pdf_path)
    pdf_base64 = base64.standard_b64encode(pdf_data).decode('utf-8')
    prompt = load_prompt(prompt_file)

    # Use Claude's PDF analysis capability with higher token limit for transcriptions
    message = client.messages.create(
        model=model,
        max_tokens=16384,
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


def save_transcription(transcription_text, output_path):
    """Save transcription to markdown file with disclaimer comment."""
    disclaimer = "<!-- This is an AI-generated transcript of a PDF. Certain elements of the original document, such as figures and images, have been replaced with descriptions. -->\n\n"

    with open(output_path, 'w') as f:
        f.write(disclaimer + transcription_text)
