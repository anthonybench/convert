"""HTML and PDF conversion logic."""

from __future__ import annotations

from pathlib import Path

from sleepyconvert.utils.doc_shared import convertHtmlPdf as convertHtmlPdfPair


def convertHtmlPdf(input_path: Path, output_path: Path) -> None:
    """Convert between HTML and PDF document files.

    Parameters:
        input_path: The source file path.
        output_path: The destination file path.

    Returns:
        None.
    """

    convertHtmlPdfPair(input_path=input_path, output_path=output_path)
