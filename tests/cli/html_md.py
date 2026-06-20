"""CLI tests for HTML and Markdown conversions."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from sleepyconvert.main import app

runner = CliRunner()


def testHtmlToMd(tmp_path: Path) -> None:
    """Verify HTML files can be converted into Markdown files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.html"
    output_path = tmp_path / "sample.md"
    input_path.write_text("<h1>Hello</h1><p>World</p>", encoding="utf-8")

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "Hello" in content
    assert "World" in content


def testMdToHtml(tmp_path: Path) -> None:
    """Verify Markdown files can be converted into HTML files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.md"
    output_path = tmp_path / "sample.html"
    input_path.write_text("# Hello\n\nWorld", encoding="utf-8")

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "<h1>" in content
    assert "World" in content
