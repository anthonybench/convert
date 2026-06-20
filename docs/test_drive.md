# Test Drive

## Setup

Install the package in editable mode with dev dependencies:

```bash
pip install -e ".[dev]"
```

This registers the `sleepyconvert` CLI command and lets you edit source files without reinstalling.

## Running Tests

```bash
pytest
```

Tests live in `tests/` and use `tmp_path` fixtures — no setup or cleanup needed.

Test modules mirror their handler by name (no `test_` prefix), so run a single pair like this:

```bash
pytest tests/cli/csv_parquet.py
```

## End-to-End Conversion Harness

To exercise the real CLI against the fixtures in `_ephemeral/test_data/` and verify the outputs:

```bash
./tools/test.sh
```

It converts each data fixture to CSV, each document fixture to Markdown, and each image fixture to the other raster format under `_ephemeral/test_output/`, then runs `tools/_verify_test.py` to confirm every output matches its source.

## Using the CLI

```bash
sleepyconvert <input_path> <output_path>
```

Both paths must include extensions, and the extensions must belong to the same category (see below).

**Examples:**

```bash
sleepyconvert data.csv data.parquet
sleepyconvert report.md report.pdf
sleepyconvert photo.png photo.jpg
```

**Help:**

```bash
sleepyconvert --help
```

## Supported Conversions

| Category  | Extensions                              |
| --------- | --------------------------------------- |
| Data      | `csv`, `json`, `parquet`, `pkl`, `xlsx` |
| Images    | `png`, `jpg`, `jpeg`                    |
| Documents | `html`, `md`, `pdf`                     |

Any pair within the same category is valid; cross-category conversions are rejected.

## Formatting

```bash
./tools/format.sh
```

Runs `shfmt` on shell scripts, `black` on Python files, and `prettier` on Markdown.
