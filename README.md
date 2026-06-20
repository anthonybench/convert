# sleepyconvert

`sleepyconvert` is a succinct [Typer](https://typer.tiangolo.com/)-based CLI that converts data files, images, and documents between formats, inferring intent solely from the input and output extensions.

## Supported conversions

- Data: `csv`, `parquet`, `json`, `pkl`, `xlsx`
- Images: `png`, `jpg`, `jpeg`
- Documents: `html`, `pdf`, `md`

Formats can only be converted within the same category.

## Install

```sh
pip install sleepyconvert
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

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Then run `pytest`, or `./tools/test.sh` to exercise the CLI end to end. Tear down with `deactivate && rm -rf .venv`.

## Documentation

- [Specification](docs/SPEC.md) — what the tool does
- [Project outline](docs/OUTLINE.md) — repository layout
- [Test drive](docs/test_drive.md) — setup, testing, and CLI usage
- [Publishing](docs/publish.md) — release to PyPI with Poetry
