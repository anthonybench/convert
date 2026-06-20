"""Shared helpers for tabular data conversions."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def readDataFrame(input_path: Path) -> pd.DataFrame:
    """Read a supported data file into a pandas DataFrame.

    Parameters:
        input_path: The source data file path.

    Returns:
        The loaded DataFrame.
    """

    match input_path.suffix.lower():
        case ".csv":
            return pd.read_csv(input_path)
        case ".json":
            return pd.read_json(input_path)
        case ".parquet":
            return pd.read_parquet(input_path)
        case ".pkl":
            return pd.read_pickle(input_path)
        case ".xlsx":
            return pd.read_excel(input_path)
        case _:
            raise ValueError(f"Unsupported data input format: {input_path.suffix}")


def writeDataFrame(data_frame: pd.DataFrame, output_path: Path) -> None:
    """Write a pandas DataFrame to a supported data file format.

    Parameters:
        data_frame: The DataFrame to serialize.
        output_path: The destination data file path.

    Returns:
        None.
    """

    match output_path.suffix.lower():
        case ".csv":
            data_frame.to_csv(output_path, index=False)
        case ".json":
            data_frame.to_json(output_path, orient="records", indent=2)
        case ".parquet":
            data_frame.to_parquet(output_path, index=False)
        case ".pkl":
            data_frame.to_pickle(output_path)
        case ".xlsx":
            data_frame.to_excel(output_path, index=False)
        case _:
            raise ValueError(f"Unsupported data output format: {output_path.suffix}")


def convertDataPair(input_path: Path, output_path: Path) -> None:
    """Convert between two supported tabular data formats.

    Parameters:
        input_path: The source data file path.
        output_path: The destination data file path.

    Returns:
        None.
    """

    data_frame = readDataFrame(input_path=input_path)
    writeDataFrame(data_frame=data_frame, output_path=output_path)
