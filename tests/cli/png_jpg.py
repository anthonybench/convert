"""CLI tests for PNG and JPEG conversions."""

from __future__ import annotations

from pathlib import Path

from PIL import Image
from typer.testing import CliRunner

from sleepyconvert.main import app

runner = CliRunner()


def testPngToJpg(tmp_path: Path) -> None:
    """Verify PNG files can be converted into JPG files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.png"
    output_path = tmp_path / "sample.jpg"
    Image.new("RGB", (10, 10), color=(255, 0, 0)).save(input_path)

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    with Image.open(output_path) as image:
        assert image.format == "JPEG"


def testJpgToPng(tmp_path: Path) -> None:
    """Verify JPG files can be converted into PNG files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.jpg"
    output_path = tmp_path / "sample.png"
    Image.new("RGB", (10, 10), color=(0, 255, 0)).save(input_path)

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    with Image.open(output_path) as image:
        assert image.format == "PNG"


def testPngToJpeg(tmp_path: Path) -> None:
    """Verify PNG files can be converted into JPEG files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.png"
    output_path = tmp_path / "sample.jpeg"
    Image.new("RGB", (10, 10), color=(0, 0, 255)).save(input_path)

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    with Image.open(output_path) as image:
        assert image.format == "JPEG"


def testJpegToJpg(tmp_path: Path) -> None:
    """Verify JPEG files can be converted into JPG files.

    Parameters:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.jpeg"
    output_path = tmp_path / "sample.jpg"
    Image.new("RGB", (10, 10), color=(128, 128, 0)).save(input_path)

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    with Image.open(output_path) as image:
        assert image.format == "JPEG"
