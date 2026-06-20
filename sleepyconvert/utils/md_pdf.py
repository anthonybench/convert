"""Markdown and PDF conversion logic."""

from __future__ import annotations

from pathlib import Path

from sleepyconvert.utils.doc_shared import convertMdPdf as convertMdPdfPair


def convertMdPdf(input_path: Path, output_path: Path) -> None:
    """Convert between Markdown and PDF document files.

    Parameters:
        input_path: The source file path.
        output_path: The destination file path.

    Returns:
        None.
    """

    convertMdPdfPair(input_path=input_path, output_path=output_path)
