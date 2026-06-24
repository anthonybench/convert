"""Tests for the shared sleepy params loading and convert config wiring."""

from __future__ import annotations

from pathlib import Path

import pytest

from sleepyconvert.core.config import loadAppConfig
from sleepyconvert.core.sleepy_params import (
    PARAMS_PATH_ENV_VAR,
    loadSleepyParams,
)


def testLoadSleepyParamsWritesDefaultsWhenMissing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Ensure a missing params file is created with defaults and announced.

    Parameters:
        tmp_path: Pytest temporary directory fixture.
        monkeypatch: Pytest monkeypatch fixture.

    Returns:
        None.
    """

    params_path = tmp_path / "fresh" / "params.yml"
    monkeypatch.setenv(PARAMS_PATH_ENV_VAR, str(params_path))

    messages: list[str] = []
    params = loadSleepyParams(echo=messages.append)

    assert params_path.exists()
    assert params["convert_output_archive_dir"] is None
    assert any("defaults" in message for message in messages)


def testLoadAppConfigReadsArchiveDir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure the configured archive directory is surfaced on the app config.

    Parameters:
        tmp_path: Pytest temporary directory fixture.
        monkeypatch: Pytest monkeypatch fixture.

    Returns:
        None.
    """

    archive_dir = tmp_path / "archive"
    params_path = tmp_path / "custom" / "params.yml"
    params_path.parent.mkdir(parents=True, exist_ok=True)
    params_path.write_text(
        f"convert_output_archive_dir: {archive_dir}\n",
        encoding="utf-8",
    )
    monkeypatch.setenv(PARAMS_PATH_ENV_VAR, str(params_path))

    config = loadAppConfig()

    assert config.output_archive_dir == archive_dir


def testLoadAppConfigArchiveDirDefaultsToNone() -> None:
    """Ensure archiving is disabled by default.

    Returns:
        None.
    """

    config = loadAppConfig()

    assert config.output_archive_dir is None
