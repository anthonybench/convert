"""CLI tests for CSV and JSON conversions."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from sleepyconvert.main import app

runner = CliRunner()


def testCsvToJson(tmp_path: Path) -> None:
    """Verify CSV files can be converted into JSON files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.csv"
    output_path = tmp_path / "sample.json"
    input_path.write_text("name,value\nalpha,1\nbeta,2\n", encoding="utf-8")

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    records = json.loads(output_path.read_text(encoding="utf-8"))
    assert [r["name"] for r in records] == ["alpha", "beta"]


def testJsonToCsv(tmp_path: Path) -> None:
    """Verify JSON files can be converted into CSV files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.json"
    output_path = tmp_path / "sample.csv"
    input_path.write_text(
        json.dumps([{"name": "gamma", "value": 3}, {"name": "delta", "value": 4}]),
        encoding="utf-8",
    )

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "name,value"
    assert "gamma" in lines[1]
