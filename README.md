# sleepyconvert

`sleepyconvert` is a succinct [Typer](https://typer.tiangolo.com/)-based CLI that converts data files, images, and documents between formats, inferring intent solely from the input and output extensions.

## Supported conversions

- Data: `csv`, `parquet`, `json`, `pkl`, `xlsx`
- Images: `png`, `jpg`, `jpeg`
- Documents: `html`, `pdf`, `md`

Formats can only be converted within the same category.

## Install

Install the CLI globally with [uv](https://docs.astral.sh/uv/):

```sh
uv tool install sleepyconvert
```

## Usage

```sh
sleepyconvert <input_path> <output_path>
```

The tool takes exactly two arguments — there is no subcommand. Both paths are resolved relative to the current working directory, and their extensions must belong to the same category.

```sh
sleepyconvert data.csv data.parquet
sleepyconvert report.md report.pdf
sleepyconvert photo.png photo.jpg
sleepyconvert --help
```

## Development

Create the environment and install in editable mode with [uv](https://docs.astral.sh/uv/):

```sh
uv venv
uv pip install -e ".[dev]"
```

Then run `uv run pytest`, or `./tools/test.sh` to exercise the CLI end to end. Tear down with `rm -rf .venv`.

## Configuration

`sleepyconvert` is a *sleepy util* and reads its settings from the shared
`~/sleepyconfig/params.yml`. Each sleepy util owns only its own `<tool>_<name>`
keys; sleepyconvert uses the `convert_` prefix. If the file is absent,
sleepyconvert writes only its own section and prints a note. If a value it
needs is missing, it prints that section and asks you to verify your config.
Key:

- `convert_output_archive_dir` — when set to a directory, every conversion also
  writes a dated copy of its output there as
  `<archive_dir>/<yyyy>_<mm>_<dd>_<output_filename>`. Leave as `null` to disable.

```yaml
# sleepyconvert
convert_output_archive_dir: null
```

## Documentation

- [Specification](docs/SPEC.md) — what the tool does
- [Project outline](docs/OUTLINE.md) — repository layout
- [Test drive](docs/test_drive.md) — setup, testing, and CLI usage
- [Publishing](docs/publish.md) — release to PyPI with Poetry
