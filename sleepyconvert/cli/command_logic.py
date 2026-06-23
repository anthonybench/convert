"""Argument parsing and dispatch logic for the sleepyconvert CLI."""

from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path
from typing import Callable

import typer

from sleepyconvert.core.config import AppConfig, loadAppConfig
from sleepyconvert.core.logging import getLogger, setupLogging
from sleepyconvert.utils import getConversionHandler

ConversionHandler = Callable[[Path, Path], None]


def _normalizeExtension(path: Path) -> str:
    """Return the normalized file extension for a path.

    Parameters:
        path: The file path whose extension should be normalized.

    Returns:
        The lowercase extension without the leading dot.
    """

    return path.suffix.lower().lstrip(".")


def _validatePaths(
    input_file_path: Path,
    output_file_path: Path,
    config: AppConfig,
) -> tuple[str, str, str]:
    """Validate the input and output paths and resolve their conversion category.

    Parameters:
        input_file_path: The provided source file path.
        output_file_path: The provided destination file path.
        config: Application configuration containing supported extensions.

    Returns:
        A tuple of input extension, output extension, and shared file category.
    """

    input_extension = _normalizeExtension(input_file_path)
    output_extension = _normalizeExtension(output_file_path)

    if not input_extension or not output_extension:
        raise typer.BadParameter("Both input and output paths must include a file extension.")

    input_category = config.getCategoryForExtension(input_extension)
    output_category = config.getCategoryForExtension(output_extension)

    if input_category is None:
        raise typer.BadParameter(f"Unsupported input extension: .{input_extension}")

    if output_category is None:
        raise typer.BadParameter(f"Unsupported output extension: .{output_extension}")

    if input_category != output_category:
        raise typer.BadParameter(
            "Input and output extensions must belong to the same type group. "
            "Use `convert --help` to see the supported categories."
        )

    if input_extension == output_extension:
        raise typer.BadParameter("Input and output extensions must be different.")

    return input_extension, output_extension, input_category


def _prepareOutputDirectory(output_file_path: Path) -> None:
    """Create the destination directory when it does not already exist.

    Parameters:
        output_file_path: The output file path whose parent directory should exist.

    Returns:
        None.
    """

    output_file_path.parent.mkdir(parents=True, exist_ok=True)


def _archiveOutput(output_file_path: Path, archive_dir: Path) -> Path:
    """Write a dated copy of the conversion output into the archive directory.

    The archived file is named ``<yyyy>_<mm>_<dd>_<output_filename>`` and placed
    inside ``archive_dir``.

    Parameters:
        output_file_path: The freshly written conversion output.
        archive_dir: The directory to receive the dated copy.

    Returns:
        The path of the archived copy.
    """

    archive_dir.mkdir(parents=True, exist_ok=True)
    stamp = date.today().strftime("%Y_%m_%d")
    archive_path = archive_dir / f"{stamp}_{output_file_path.name}"
    shutil.copy2(output_file_path, archive_path)
    return archive_path


def runConversion(input_path: str, output_path: str) -> None:
    """Validate arguments and perform the requested conversion.

    Parameters:
        input_path: The source file path provided on the command line.
        output_path: The destination file path provided on the command line.

    Returns:
        None.
    """

    config = loadAppConfig()
    setupLogging(log_level=config.log_level)
    logger = getLogger(__name__)

    input_file_path = Path(input_path).expanduser().resolve()
    output_file_path = Path(output_path).expanduser().resolve()

    input_extension, output_extension, file_category = _validatePaths(
        input_file_path=input_file_path,
        output_file_path=output_file_path,
        config=config,
    )

    if not input_file_path.exists():
        raise typer.BadParameter(f"Input file does not exist: {input_file_path}")

    handler: ConversionHandler = getConversionHandler(
        input_extension=input_extension,
        output_extension=output_extension,
    )

    _prepareOutputDirectory(output_file_path)
    logger.info(
        "Converting %s file from .%s to .%s",
        file_category,
        input_extension,
        output_extension,
    )
    handler(input_file_path, output_file_path)
    typer.echo(f"Created {output_file_path}")

    if config.output_archive_dir is not None:
        archive_path = _archiveOutput(output_file_path, config.output_archive_dir)
        typer.echo(f"Archived copy written to {archive_path}")
