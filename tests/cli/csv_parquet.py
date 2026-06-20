"""CLI tests for CSV and Parquet conversions."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from sleepyconvert.main import app

runner = CliRunner()


def testCsvToParquet(tmp_path: Path) -> None:
    """Verify CSV files can be converted into Parquet files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.csv"
    output_path = tmp_path / "sample.parquet"
    input_path.write_text("name,value\nalpha,1\nbeta,2\n", encoding="utf-8")

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    data_frame = pd.read_parquet(output_path)
    assert list(data_frame["name"]) == ["alpha", "beta"]


def testParquetToCsv(tmp_path: Path) -> None:
    """Verify Parquet files can be converted into CSV files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.parquet"
    output_path = tmp_path / "sample.csv"
    source_frame = pd.DataFrame({"name": ["gamma", "delta"], "value": [3, 4]})
    source_frame.to_parquet(input_path, index=False)

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    data_frame = pd.read_csv(output_path)
    assert list(data_frame["value"]) == [3, 4]


def testRejectsCrossTypeConversion(tmp_path: Path) -> None:
    """Verify the CLI rejects conversions across different type groups.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.csv"
    output_path = tmp_path / "sample.png"
    input_path.write_text("name,value\nalpha,1\n", encoding="utf-8")

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code != 0
    assert "supported categories" in result.stdout
