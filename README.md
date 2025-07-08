# Online Bookstore - Test Automation Framework

[![CI/CD](https://github.com/sodelalbert/online_bookstore_taf/actions/workflows/ci.yml/badge.svg)](https://github.com/sodelalbert/online_bookstore_taf/actions/workflows/ci.yml)

- Technologies used.

## Project Structure

- markers: api, ui, e2e, smoke

```bash
uv run pytest -m api
```

## Installation & Configuration

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

## Running Test Cases

- Automatic python installation
- Automatic dependency instlalation

```bash
uv run pytest
```

## Pipeline Integration and Reporting

- Dependednt jobs etc.

- pipeline print screen & Artifacts

- `reports` & `report.htmml`

## Code Standard & Contribution

- black, pylint, mypy
- `precommit.sh`
