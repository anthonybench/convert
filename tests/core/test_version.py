"""Tests for version reporting and the -v/--version pre-scan."""

from __future__ import annotations

import sys

import pytest

import sleepyconvert.main as main_module
from sleepyconvert.core import version as version_module


def testWantsVersionDetectsFlagAnywhere() -> None:
    """-v/--version is detected even alongside the input/output paths."""

    assert version_module.wantsVersion(["--version"])
    assert version_module.wantsVersion(["-v"])
    assert version_module.wantsVersion(["a.csv", "b.parquet", "--version"])
    assert not version_module.wantsVersion(["a.csv", "b.parquet"])


def testIsNewerComparesReleases() -> None:
    """Semantic-ish comparison of dotted versions."""

    assert version_module.isNewer("2.4.0", "2.3.1")
    assert not version_module.isNewer("2.3.1", "2.3.1")
    assert not version_module.isNewer("2.3.0", "2.3.1")


def testPrintVersionQuietWhenCheckFails(capsys: pytest.CaptureFixture[str]) -> None:
    """A failed update check prints only the version line (graceful)."""

    version_module.printVersion(fetch_latest=lambda: None)

    out = capsys.readouterr().out
    assert version_module.DIST_NAME in out
    assert "newer version" not in out


def testPrintVersionFlagsNewerRelease(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A newer published version is surfaced with an upgrade hint."""

    monkeypatch.setattr(version_module, "getVersion", lambda: "1.0.0")
    version_module.printVersion(fetch_latest=lambda: "999.0.0")

    assert "newer version is available: 999.0.0" in capsys.readouterr().out


def testLatestVersionReturnsNoneOnNetworkFailure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Any error during the PyPI lookup yields None rather than raising."""

    def _boom(*args, **kwargs):
        raise OSError("no network")

    monkeypatch.setattr(version_module.urllib.request, "urlopen", _boom)
    assert version_module.latestVersion() is None


def testRunVersionShortCircuits(monkeypatch: pytest.MonkeyPatch) -> None:
    """--version alongside paths prints version and never runs the conversion."""

    calls = {"app": False, "version": False}
    monkeypatch.setattr(main_module, "app", lambda: calls.__setitem__("app", True))
    monkeypatch.setattr(main_module, "printVersion", lambda: calls.__setitem__("version", True))
    monkeypatch.setattr(sys, "argv", ["sleepyconvert", "a.csv", "b.parquet", "--version"])

    main_module.run()

    assert calls == {"app": False, "version": True}


def testRunRunsAppWithoutVersion(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without the flag, the Typer app is invoked as usual."""

    calls = {"app": False, "version": False}
    monkeypatch.setattr(main_module, "app", lambda: calls.__setitem__("app", True))
    monkeypatch.setattr(main_module, "printVersion", lambda: calls.__setitem__("version", True))
    monkeypatch.setattr(sys, "argv", ["sleepyconvert", "a.csv", "b.parquet"])

    main_module.run()

    assert calls == {"app": True, "version": False}
