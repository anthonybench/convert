<div align="center">

# 🔄 sleepyconvert

**Convert data, images, and documents between formats from one terse CLI.**

[![PyPI](https://img.shields.io/pypi/v/sleepyconvert.svg)](https://pypi.org/project/sleepyconvert/)
[![Python](https://img.shields.io/pypi/pyversions/sleepyconvert.svg)](https://pypi.org/project/sleepyconvert/)
[![License](https://img.shields.io/badge/license-GPL--3.0--or--later-blue.svg)](LICENSE)

</div>

`sleepyconvert` is a [Typer](https://typer.tiangolo.com/) CLI that converts files between formats, inferring intent **solely from the input and output extensions** — no subcommands, no flags to memorize. Point it at a source and a destination and it does the right thing.

## Install

```sh
uv tool install sleepyconvert     # or: pipx install sleepyconvert
```

> `-v` / `--version` prints the version and best-effort checks PyPI for a newer release — it works even when placed alongside the paths. Run `sleepyconvert about` for the project's PyPI + GitHub links.

## Configure

`sleepyconvert` is a _sleepy util_ and reads its settings from the shared `~/sleepyconfig/params.yml`, using the `convert_` key prefix. If the file is absent it writes **only its own section** (below) and says so; if a value it needs is missing it prints this snippet and asks you to verify your config.

```yaml
# sleepyconvert
convert_output_archive_dir: null   # a dir → also save a dated copy of every output; null → off
```

- **`convert_output_archive_dir`** — when set to a directory, every conversion also drops a dated copy of its output there as `<archive_dir>/<yyyy>_<mm>_<dd>_<output_filename>`.

## Supported conversions

| Category | Extensions |
| --- | --- |
| **Data** | `csv`, `parquet`, `json`, `pkl`, `xlsx` |
| **Images** | `png`, `jpg`, `jpeg` |
| **Documents** | `html`, `pdf`, `md` |

Any pair **within the same category** is valid (in either direction); cross-category conversions are rejected.

## Usage

```sh
sleepyconvert <input_path> <output_path>
```

Both paths resolve relative to the current directory, and their extensions decide the conversion.

**Data** — round-trip between tabular formats:

```console
$ sleepyconvert sales.csv sales.parquet
Created /Users/dingus/work/sales.parquet
```

**Images** — re-encode between raster formats:

```console
$ sleepyconvert photo.png photo.jpg
Created /Users/dingus/pics/photo.jpg
```

**Documents** — convert between markup and PDF:

```console
$ sleepyconvert notes.md notes.pdf
Created /Users/dingus/docs/notes.pdf
```

With `convert_output_archive_dir` set, each conversion also writes a dated archive copy:

```console
$ sleepyconvert sales.csv sales.parquet
Created /Users/dingus/work/sales.parquet
Archived copy written to /Users/dingus/archive/2026_02_09_sales.parquet
```

Mixing categories fails fast with a clear message:

```console
$ sleepyconvert data.csv chart.png
Error: Input and output extensions must belong to the same type group.
Use `convert --help` to see the supported categories.
```

**About** — print the version and the project's public PyPI + GitHub links:

```console
$ sleepyconvert about
sleepyconvert 2.3.1
PyPI:   https://pypi.org/project/sleepyconvert/
GitHub: https://github.com/anthonybench/convert
```

## Development

```sh
uv venv
uv pip install -e ".[dev]"
uv run pytest          # or ./tools/test.sh
```

## Documentation

- [Specification](docs/SPEC.md) — what the tool does
- [Project outline](docs/OUTLINE.md) — repository layout
- [Test drive](docs/test_drive.md) — setup, testing, and CLI usage
- [Adding a conversion](docs/new_command.md) — how to add a new format pair
- [Publishing](docs/publish.md) — release to PyPI
