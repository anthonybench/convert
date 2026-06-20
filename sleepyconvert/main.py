"""CLI entrypoint for the sleepyconvert application."""

from __future__ import annotations

import typer

from sleepyconvert.cli.command_logic import runConversion

app = typer.Typer(
    add_completion=False,
    help="Convert files between supported formats by passing an input and output path.",
)


@app.command(name="")
def main(input_path: str, output_path: str) -> None:
    """Convert a file into another file of the same supported type."""

    runConversion(input_path=input_path, output_path=output_path)


def run() -> None:
    """Run the Typer application."""

    app()


if __name__ == "__main__":
    run()
