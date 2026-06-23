"""CLI tests for the output archive feature."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest
from typer.testing import CliRunner

from sleepyconvert.core.sleepy_params import PARAMS_PATH_ENV_VAR
from sleepyconvert.main import app

runner = CliRunner()


def testConversionWritesArchiveCopyWhenConfigured(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify a dated archive copy is written when an archive dir is set.

    Parameters:
        tmp_path: Temporary directory provided by pytest.
        monkeypatch: Pytest monkeypatch fixture.

    Returns:
        None.
    """

    archive_dir = tmp_path / "archive"
    params_path = tmp_path / "params.yml"
    params_path.write_text(
        f"convert_output_archive_dir: {archive_dir}\n",
        encoding="utf-8",
    )
    monkeypatch.setenv(PARAMS_PATH_ENV_VAR, str(params_path))

    input_path = tmp_path / "sample.csv"
    output_path = tmp_path / "sample.json"
    input_path.write_text("name,value\nalpha,1\n", encoding="utf-8")

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()

    stamp = date.today().strftime("%Y_%m_%d")
    archive_path = archive_dir / f"{stamp}_sample.json"
    assert archive_path.exists()
    assert json.loads(archive_path.read_text(encoding="utf-8")) == json.loads(
        output_path.read_text(encoding="utf-8")
    )


def testConversionSkipsArchiveWhenUnset(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify no archive copy is written when the archive dir is null.

    Parameters:
        tmp_path: Temporary directory provided by pytest.
        monkeypatch: Pytest monkeypatch fixture.

    Returns:
        None.
    """

    params_path = tmp_path / "params.yml"
    params_path.write_text("convert_output_archive_dir: null\n", encoding="utf-8")
    monkeypatch.setenv(PARAMS_PATH_ENV_VAR, str(params_path))

    input_path = tmp_path / "sample.csv"
    output_path = tmp_path / "sample.json"
    input_path.write_text("name,value\nalpha,1\n", encoding="utf-8")

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert "Archived copy" not in result.stdout
