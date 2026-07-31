"""CLI entrypoint for the sleepyconvert application."""

from __future__ import annotations

import sys

import typer

from sleepyconvert.cli.command_logic import runConversion
from sleepyconvert.core.version import printVersion, wantsVersion

app = typer.Typer(
    add_completion=False,
    help=(
        "Convert files between supported formats by passing an input and output path. "
        "Pass -v/--version to print the version."
    ),
)


@app.command(name="")
def main(input_path: str, output_path: str) -> None:
    """Convert a file into another file of the same supported type."""

    runConversion(input_path=input_path, output_path=output_path)


def run() -> None:
    """Run the Typer application.

    ``-v``/``--version`` is honored before Typer parses, so it works even when it
    appears alongside the paths; the conversion is skipped.
    """

    if wantsVersion(sys.argv[1:]):
        printVersion()
        return
    app()


if __name__ == "__main__":
    run()
