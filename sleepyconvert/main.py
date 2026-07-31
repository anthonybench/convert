"""CLI entrypoint for the sleepyconvert application."""

from __future__ import annotations

import sys

import typer

from sleepyconvert.cli.command_logic import runConversion
from sleepyconvert.core.about import printAbout, wantsAbout
from sleepyconvert.core.version import printVersion, wantsVersion

app = typer.Typer(
    add_completion=False,
    help=(
        "Convert files between supported formats by passing an input and output path. "
        "Pass -v/--version to print the version, or `about` for project links."
    ),
)


@app.command(name="")
def main(input_path: str, output_path: str) -> None:
    """Convert a file into another file of the same supported type."""

    runConversion(input_path=input_path, output_path=output_path)


def run() -> None:
    """Run the Typer application.

    ``-v``/``--version`` and the ``about`` pseudo-command are honored before Typer
    parses (sleepyconvert is a single-command CLI, so they can't be real
    subcommands); when present, the conversion is skipped.
    """

    args = sys.argv[1:]
    if wantsVersion(args):
        printVersion()
        return
    if wantsAbout(args):
        printAbout()
        return
    app()


if __name__ == "__main__":
    run()
