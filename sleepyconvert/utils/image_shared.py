"""Shared helpers for image conversions."""

from __future__ import annotations

from pathlib import Path

from PIL import Image


def convertRasterImage(input_path: Path, output_path: Path) -> None:
    """Convert between supported raster image formats.

    Parameters:
        input_path: The source image path.
        output_path: The destination image path.

    Returns:
        None.
    """

    with Image.open(input_path) as image:
        if output_path.suffix.lower() in {".jpg", ".jpeg"}:
            converted_image = image.convert("RGB")
        else:
            converted_image = image

        converted_image.save(output_path)
