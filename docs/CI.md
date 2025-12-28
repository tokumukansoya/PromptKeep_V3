# Continuous Integration (CI) for PromptKeep

This document explains how to use GitHub Actions to support Document-Driven Development (DDD) and automated checks for PromptKeep.

This file complements the workflow file at [`.github/workflows/ci.yml`](.github/workflows/ci.yml:1) and the project README at [`PromptKeep_V3/README.md`](PromptKeep_V3/README.md:1).

## Goals

- Ensure docs-first development: documentation changes are required and validated before or together with implementation.
- Run linters, tests and basic smoke checks on push and pull request events.
- Provide reproducible CI suitable for AI-assisted and human development.

## Triggers

Run CI for:

- push and pull_request on `main` and `phase-*` branches.
- scheduled nightly runs (optional) to catch regressions early.

## Strategy

1. Docs-first gate: if a PR changes code without corresponding docs updates, CI reports a warning/failure. Use a simple file-pattern check to detect `docs/` modifications.
2. Verify environment: use Python 3.14 matrix to mirror development environment.
3. Steps: checkout, cache dependencies, set up Python, install `uv` and project dependencies, run formatters/linters/pre-commit, run tests, collect and publish test reports.

## Example workflow snippet

[`yaml`](.github/workflows/ci.yml:1)

```yaml
name: CI

on:
  push:
    branches:
      - main
      - 'phase-*'
  pull_request:
    branches:
      - main
      - 'phase-*'
  schedule:
    - cron: '0 0 * * *' # optional nightly

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: [3.14]

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python }}

      - name: Cache pip/uv cache
        uses: actions/cache@v4
        with:
          path: |
            ~/.cache/pip
            ~/.uv
          key: ${{ runner.os }}-pip-${{ hashFiles('**/pyproject.toml', '**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies (uv)
        run: |
          python -m pip install --upgrade pip
          pip install uv
          uv sync || true
          uv run python -m pip install -r requirements.txt || true

      - name: Run pre-commit (linters & formatters)
        run: |
          pip install pre-commit
          pre-commit run --all-files || true

      - name: Run tests
        run: |
          uv run python -m pytest -q --junitxml=reports/test-results.xml

      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: reports/test-results.xml

      - name: Docs-first check
        run: |
          # Fail the job if code changes exist without doc updates.
          # This is a simple heuristic: if files under src/ or PromptKeep_V3/ changed and docs/ did not, fail.
          git fetch --no-tags origin ${{ github.base_ref }} || true
          CHANGED_FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD || true)
          echo "$CHANGED_FILES" > changed.txt
          if echo "$CHANGED_FILES" | grep -E "(^|/)PromptKeep_V3/|(^|/)src/" >/dev/null && ! echo "$CHANGED_FILES" | grep -E "(^|/)docs/|(^|/)README.md" >/dev/null; then
            echo "Code changed without docs updates. Please update docs in docs/ or README.md" >&2
            exit 1
          fi
```

Adjust path patterns above to match your repository layout if needed.

## Pull Request checklist (recommended)

Add this to PR templates or use it in reviewer guidance:

- [ ] Update relevant docs in `docs/` or `README.md` for the change
- [ ] Add or update tests in `tests/`
- [ ] Run `uv sync` and `uv run pytest` locally
- [ ] Confirm linters/formatters pass
- [ ] Use Conventional Commit style (e.g. `docs:`, `feat:`, `fix:`)

## Locally running CI steps

To reproduce CI locally:

- Install Python 3.14
- pip install uv
- uv sync
- uv run python -m pytest
- pip install pre-commit
- pre-commit run --all-files

## Badges

Add a status badge to the [`README.md`](PromptKeep_V3/README.md:1):

[![CI](https://github.com/<your-org>/<your-repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<your-org>/<your-repo>/actions)

Replace `<your-org>/<your-repo>` with your repository path.

## Troubleshooting

- If tests are flaky, use the `schedule` nightly run to surface intermittent failures.
- If the `Docs-first check` is too strict, change it to issue a warning only (remove `exit 1`).

## Next steps (recommended)

- Update [`.github/workflows/ci.yml`](.github/workflows/ci.yml:1) to match the example and commit as `ci: add workflow`.
- Add a PR template that includes the Pull Request checklist.
- Add a short section in [`README.md`](PromptKeep_V3/README.md:1) describing Document-Driven Development and linking to this file.

**Last updated**: 2025-12-28
