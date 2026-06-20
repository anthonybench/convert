"""CLI tests for Parquet and Excel conversions."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from sleepyconvert.main import app

runner = CliRunner()


def testParquetToXlsx(tmp_path: Path) -> None:
    """Verify Parquet files can be converted into Excel files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.parquet"
    output_path = tmp_path / "sample.xlsx"
    source_frame = pd.DataFrame({"name": ["alpha", "beta"], "value": [1, 2]})
    source_frame.to_parquet(input_path, index=False)

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    data_frame = pd.read_excel(output_path)
    assert list(data_frame["name"]) == ["alpha", "beta"]


def testXlsxToParquet(tmp_path: Path) -> None:
    """Verify Excel files can be converted into Parquet files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.xlsx"
    output_path = tmp_path / "sample.parquet"
    source_frame = pd.DataFrame({"name": ["gamma", "delta"], "value": [3, 4]})
    source_frame.to_excel(input_path, index=False)

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    data_frame = pd.read_parquet(output_path)
    assert list(data_frame["value"]) == [3, 4]
