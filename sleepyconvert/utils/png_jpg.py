"""PNG and JPEG conversion logic."""

from __future__ import annotations

from pathlib import Path

from sleepyconvert.utils.image_shared import convertRasterImage


def convertPngJpg(input_path: Path, output_path: Path) -> None:
    """Convert between PNG and JPEG image files.

    Parameters:
        input_path: The source file path.
        output_path: The destination file path.

    Returns:
        None.
    """

    convertRasterImage(input_path=input_path, output_path=output_path)
