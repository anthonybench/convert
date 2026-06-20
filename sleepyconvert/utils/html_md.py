"""HTML and Markdown conversion logic."""

from __future__ import annotations

from pathlib import Path

from sleepyconvert.utils.doc_shared import convertHtmlMd as convertHtmlMdPair


def convertHtmlMd(input_path: Path, output_path: Path) -> None:
    """Convert between HTML and Markdown document files.

    Parameters:
        input_path: The source file path.
        output_path: The destination file path.

    Returns:
        None.
    """

    convertHtmlMdPair(input_path=input_path, output_path=output_path)
