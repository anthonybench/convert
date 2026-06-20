# AGENTS.md

## Python

- always use `camelCase` for function names.
- always use `PascalCase` for class and component names.
- always use `lower_snake_case` for variable names.
- prefer `case` over `if/elif` blocks for conditional logic when there are more than 2 possibilities.
- ensure all functions have type hints for arguments and return types.
- avoid using `any` type; always strive for exact type hinting.
- always add docstrings to all functions and classes explaining their purpose, parameters, and return values.

## Shell Script

- always put variables at the top in `UPPER_SNAKE_CASE`
- be sparing and succinct with comments, only when a line of code is dense or unintuitive
- the shebang should be `#!/bin/zsh`

## Documentation

- `README.md` :: succinct project overview, and steps to deploy/teardown the project
- `docs/*.md` :: succinct documentation, preferring files to be single-purposed, meaning it is more desired to have many small files that humans can read quickly rather than fewer larger files that humans have to navigate through

## Tooling

- `tools/*` :: scripts for humans to run, must have a readme comment block in the form:

  ```
  <tool_title>

  <description>

  Usage:
      <cli_tool_usage>
  ```

  - there should be a tool `format.sh` that formats:
    - all shell scripts with `shfmt`
    - all python files with `black`
    - all markdown files with `prettier`
