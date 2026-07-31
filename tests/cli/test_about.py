"""Tests for the ``about`` pseudo-command."""

from __future__ import annotations

import sys

import pytest

import sleepyconvert.main as main_module
from sleepyconvert.core import about as about_module


def testAboutPrintsPublicLinks(capsys: pytest.CaptureFixture[str]) -> None:
    """`printAbout` emits the PyPI and GitHub URLs."""

    about_module.printAbout()

    out = capsys.readouterr().out
    assert "https://pypi.org/project/sleepyconvert/" in out
    assert "github.com/anthonybench/convert" in out


def testRunAboutShortCircuits(monkeypatch: pytest.MonkeyPatch) -> None:
    """`sleepyconvert about` prints links and never runs a conversion."""

    calls = {"app": False, "about": False}
    monkeypatch.setattr(main_module, "app", lambda: calls.__setitem__("app", True))
    monkeypatch.setattr(main_module, "printAbout", lambda: calls.__setitem__("about", True))
    monkeypatch.setattr(sys, "argv", ["sleepyconvert", "about"])

    main_module.run()

    assert calls == {"app": False, "about": True}


def testRunTreatsPathsNormally(monkeypatch: pytest.MonkeyPatch) -> None:
    """A normal two-path invocation still dispatches to the Typer app."""

    calls = {"app": False, "about": False}
    monkeypatch.setattr(main_module, "app", lambda: calls.__setitem__("app", True))
    monkeypatch.setattr(main_module, "printAbout", lambda: calls.__setitem__("about", True))
    monkeypatch.setattr(sys, "argv", ["sleepyconvert", "a.csv", "b.parquet"])

    main_module.run()

    assert calls == {"app": True, "about": False}
