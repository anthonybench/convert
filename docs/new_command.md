# Adding a Conversion

sleepyconvert has a single command — `sleepyconvert <input> <output>` — and
infers intent from the file extensions. "Adding a command" therefore means
**adding a new conversion (format pair)**, not a new subcommand.

A conversion is one handler covering both directions of an unordered extension
pair (e.g. `csv ↔ json`), registered in the handler registry. Both extensions
must belong to the same category; cross-category conversions are rejected.

## 1. Make sure both extensions are supported and in one category

Categories and their extensions live in `loadAppConfig()` in `core/config.py`:

```python
supported_extensions = {
    "data": ("csv", "parquet", "json", "pkl", "xlsx"),
    "img": ("png", "jpg", "jpeg"),
    "doc": ("html", "pdf", "md"),
}
```

If you are introducing a brand-new extension, add it to the right category here.
For a **data** extension, also add read/write branches in
`utils/data_shared.py` (`readDataFrame` / `writeDataFrame`); the document and
image categories have their own shared helpers (`doc_shared.py`,
`image_shared.py`).

## 2. Implement the handler

One file per pair: `sleepyconvert/utils/<a>_<b>.py`, exposing a handler with the
signature `(input_path: Path, output_path: Path) -> None`. It must work in both
directions — within a category that usually means delegating to the shared
converter, which already branches on the file suffix:

```python
"""CSV and TSV conversion logic."""

from __future__ import annotations

from pathlib import Path

from sleepyconvert.utils.data_shared import convertDataPair


def convertCsvTsv(input_path: Path, output_path: Path) -> None:
    """Convert between CSV and TSV data files.

    Parameters:
        input_path: The source file path.
        output_path: The destination file path.

    Returns:
        None.
    """

    convertDataPair(input_path=input_path, output_path=output_path)
```

Reuse the `*_shared.py` helpers for category logic; add direction-specific code
only when a pair genuinely needs it.

## 3. Register the handler

In `utils/__init__.py`, import the handler and add it to `_HANDLERS`, keyed by an
unordered `frozenset` of the extension pair (so one entry serves both
directions):

```python
from sleepyconvert.utils.csv_tsv import convertCsvTsv

_HANDLERS = {
    ...
    frozenset({"csv", "tsv"}): convertCsvTsv,
}
```

`getConversionHandler` looks up the pair and raises if none is registered.

## Conventions

- Follow `AGENTS.md`: `camelCase` functions, `lower_snake_case` variables, type
  hints and docstrings on everything, `case` over `if/elif` chains.
- One handler file per pair; category-wide logic belongs in `*_shared.py`.
- Handlers do the conversion only — path validation, category matching, and the
  optional output archive are handled in `cli/command_logic.py`.

## 4. Add a test

`tests/cli/<a>_<b>.py` — test modules mirror the handler file name (no `test_`
prefix; pytest is configured with `python_files = "*.py"`). Drive the real CLI
with `CliRunner` and a `tmp_path` round-trip in both directions:

```python
from pathlib import Path

from typer.testing import CliRunner

from sleepyconvert.main import app

runner = CliRunner()


def testCsvToTsv(tmp_path: Path) -> None:
    input_path = tmp_path / "sample.csv"
    output_path = tmp_path / "sample.tsv"
    input_path.write_text("name,value\nalpha,1\n", encoding="utf-8")

    result = runner.invoke(app, [str(input_path), str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
```

The autouse fixture in `tests/conftest.py` isolates the sleepy config to a temp
file, so tests never touch the real `~/sleepyconfig`.

## 5. Update docs

Add the pair to the supported-conversions tables in `README.md` and
`docs/SPEC.md`, and mention it where relevant in `docs/test_drive.md`.
