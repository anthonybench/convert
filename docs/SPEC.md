# Specification

`sleepyconvert` is a [Typer](https://typer.tiangolo.com/)-based Python CLI that converts a file from one format to another, inferring intent solely from the input and output extensions.

## Invocation

The tool exposes a single, implicit command. The user supplies exactly two positional arguments — an input path and an output path — with no subcommand:

```sh
sleepyconvert data.csv data.parquet
```

The first argument is the input path and the second is the converted output path, both resolved relative to the working directory where the command is issued.

## Conversion Rules

Supported formats are grouped into three categories:

- **data** — `csv`, `parquet`, `json`, `pkl`, `xlsx`
- **img** — `png`, `jpg`/`jpeg`
- **doc** — `html`, `pdf`, `md`

A conversion is valid only when both extensions belong to the same category. A request that crosses categories is rejected with an error and the help message:

```sh
sleepyconvert data.csv data.png   # error: data -> img is not a valid conversion
```

Within a category, any two distinct extensions form a valid conversion.

## Design Constraints

- The CLI has exactly one command so that usage stays succinct; the command is never typed explicitly — only the two arguments follow `sleepyconvert`.
- Each conversion handler covers both directions of a single pair (e.g. one handler serves both `csv` → `json` and `json` → `csv`). See [OUTLINE.md](OUTLINE.md) for where handlers live.
- Code balances simplicity with correctness and follows the conventions in [AGENTS.md](../AGENTS.md).
