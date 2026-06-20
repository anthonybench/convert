"""Parquet and XLSX conversion logic."""

from __future__ import annotations

from pathlib import Path

from sleepyconvert.utils.data_shared import convertDataPair


def convertParquetXlsx(input_path: Path, output_path: Path) -> None:
    """Convert between Parquet and XLSX data files.

    Parameters:
        input_path: The source file path.
        output_path: The destination file path.

    Returns:
        None.
    """

    convertDataPair(input_path=input_path, output_path=output_path)
