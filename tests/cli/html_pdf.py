"""CLI tests for HTML and PDF conversions."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from typer.testing import CliRunner

from sleepyconvert.main import app

runner = CliRunner()


def testHtmlToPdf(tmp_path: Path) -> None:
    """Verify HTML files can be converted into PDF files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.html"
    output_path = tmp_path / "sample.pdf"
    input_path.write_text("<h1>Hello</h1><p>World</p>", encoding="utf-8")

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    reader = PdfReader(str(output_path))
    text = "".join(page.extract_text() or "" for page in reader.pages)
    assert "Hello" in text


def testPdfToHtml(tmp_path: Path) -> None:
    """Verify PDF files can be converted into HTML files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.pdf"
    output_path = tmp_path / "sample.html"
    canvas = Canvas(str(input_path), pagesize=letter)
    canvas.drawString(72, 700, "Hello World")
    canvas.save()

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "Hello" in content
