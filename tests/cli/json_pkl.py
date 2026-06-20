"""CLI tests for JSON and Pickle conversions."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from sleepyconvert.main import app

runner = CliRunner()


def testJsonToPkl(tmp_path: Path) -> None:
    """Verify JSON files can be converted into Pickle files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.json"
    output_path = tmp_path / "sample.pkl"
    input_path.write_text(
        json.dumps([{"name": "alpha", "value": 1}, {"name": "beta", "value": 2}]),
        encoding="utf-8",
    )

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    data_frame = pd.read_pickle(output_path)
    assert list(data_frame["name"]) == ["alpha", "beta"]


def testPklToJson(tmp_path: Path) -> None:
    """Verify Pickle files can be converted into JSON files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.pkl"
    output_path = tmp_path / "sample.json"
    source_frame = pd.DataFrame({"name": ["gamma", "delta"], "value": [3, 4]})
    source_frame.to_pickle(input_path)

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    records = json.loads(output_path.read_text(encoding="utf-8"))
    assert [r["value"] for r in records] == [3, 4]
