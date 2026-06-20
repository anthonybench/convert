# Project Outline

```txt
convert/                         # repository root (PyPI package: sleepyconvert)
├── sleepyconvert/
│   ├── __init__.py
│   ├── main.py                  # Entrypoint: assembles the root app
│   ├── cli/
│   │   ├── __init__.py
│   │   └── command_logic.py     # Examines arguments and dispatches the conversion
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # App config (env vars, supported extensions)
│   │   └── logging.py           # Shared logging setup
│   └── utils/
│       ├── __init__.py          # Handler registry keyed by extension pair
│       ├── data_shared.py       # Shared helpers for tabular formats
│       ├── doc_shared.py        # Shared helpers for document formats
│       ├── image_shared.py      # Shared helpers for raster image formats
│       ├── csv_parquet.py       # One handler per pair, covering both directions
│       └── ...                  # e.g. csv_json.py, html_md.py, png_jpg.py
├── tests/
│   ├── cli/                     # One test module per conversion pair
│   └── core/
│       └── test_config.py
├── tools/                       # Human-run scripts (see AGENTS.md)
├── docs/                        # Single-purpose documentation files
├── LICENSE
├── pyproject.toml               # Poetry-managed packaging and metadata
└── README.md
```

## Conventions

- The PyPI distribution and console command are both named `sleepyconvert`; the repository folder is `convert`.
- **Handlers** live in `sleepyconvert/utils/`, one file per format pair (e.g. `csv_json.py` holds both `csv` → `json` and `json` → `csv`). Shared logic for a category sits in the `*_shared.py` modules.
- The handler registry in `sleepyconvert/utils/__init__.py` maps each unordered extension pair to its handler.
- **Tests** in `tests/cli/` mirror the handler files, one module per pair.
- Project-wide naming, documentation, and tooling rules are defined in [AGENTS.md](../AGENTS.md).
