# PromptKeep

PromptKeep is a simple desktop application for securely managing, viewing, editing, and copying AI prompts locally.

Version: 1.0.0
Status: WIP

---

## Document-Driven Development (DDD)

This project follows Document-Driven Development. Documentation must be updated before or together with code changes.

Key points:

- Edit the relevant documentation in `docs/` and commit with the prefix `docs:` before implementing code.
- Implement code and commit using Conventional Commits (e.g. `feat:`, `fix:`).
- Pull Requests should include documentation updates and tests.

See: [`docs/DOCUMENT_GUIDE.md`](PromptKeep_V3/docs/DOCUMENT_GUIDE.md:1) and [`docs/CI.md`](PromptKeep_V3/docs/CI.md:1).

---

## Continuous Integration

This repository uses GitHub Actions to enforce linting, tests, and a docs-first check. See [`docs/CI.md`](PromptKeep_V3/docs/CI.md:1) for details and the workflow template at `.github/workflows/ci.yml`.

Badges:

[![CI](https://github.com/soya/PromptKeep/actions/workflows/ci.yml/badge.svg)](https://github.com/soya/PromptKeep/actions)
[![Coverage](https://img.shields.io/badge/coverage-unknown-lightgrey.svg)](https://github.com/soya/PromptKeep/actions)

---

## Quick setup

1. Clone the repository and change directory:

   git clone <repo-url>
   cd PromptKeep_V3

2. Install uv (if needed) and sync dependencies:

   # macOS / Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   uv sync

3. Run the app:

   uv run python main.py

---

## Project layout (short)

- `main.py` — application entry
- `PromptKeep_V3/models/` — data models (Prompt, Category)
- `PromptKeep_V3/services/` — business logic
- `PromptKeep_V3/ui/` — UI components
- `docs/` — project documentation (read this first)

---

## Contribution checklist for PRs

- [ ] Documentation updated (`docs/` or `README.md`) — required
- [ ] Tests added/updated (`tests/`)
- [ ] Linters & pre-commit pass locally
- [ ] Commit messages follow Conventional Commits

---

Last updated: 2025-12-28
