# PromptKeep — Developer Quickstart (Human)

> Readable in 5 minutes — essential for new contributors

This document summarizes what a human developer must know to start contributing to PromptKeep.

---

## What is this project?

PromptKeep is a local desktop application built with Flet for managing AI prompts.

Key features:
- Display and manage prompts as cards
- Simple single-level categories
- One-click copy
- Favorites
- Trash with restore

---

## Tech stack

- Language: Python 3.14.2
- UI: Flet 0.28.3
- Package manager: uv
- Local persistence: JSON files
- Linting/formatting: ruff / pre-commit

---

## Setup

1. Clone the repository and change directory:

   git clone <repo-url>
   cd PromptKeep_V3

2. Install uv (if needed) and sync dependencies:

   # macOS / Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   uv sync

3. Run the application:

   uv run python main.py

---

## Short project layout (what to remember)

- `main.py` — application entry point
- `PromptKeep_V3/models/` — data models (Prompt, Category)
- `PromptKeep_V3/services/` — business logic
- `PromptKeep_V3/ui/` — UI components
- `docs/` — project documentation (read this first)

See [`docs/architecture.md`](architecture.md) for full structure.

---

## Development rules (3 key rules)

1. Docs-first

When changing behavior or adding features:

- Update docs first and commit with `docs:`
- Implement code and commit with `feat:` / `fix:` / `refactor:`

2. Use uv

- Add packages: `uv add <package>`
- Run the app: `uv run python main.py`
- Avoid using pip directly for dependency management in this project

3. Conventional commits

Commit message format:

<type>: <short description>

Types: feat / fix / docs / refactor / test / chore

---

## Recommended reading order

1. `README.md` — project overview and DDD approach
2. `docs/ai_execution_guide.md` — if you plan to use AI-assisted implementation
3. `docs/requirements.md` and `docs/architecture.md` — confirm scope and structure
4. `docs/coding_style.md` — coding conventions
5. `docs/CI.md` and `docs/git_workflow.md` — CI and branch rules

---

## Important design decisions (brief)

- StateManager pattern: all state mutations go through `StateManager`
- category_ids are ID-based (not names)
- Use `page.run_task()` for background tasks in Flet UIs
- Categories are single-level (flat)

---

## Development flow (docs-first)

1. Edit the relevant docs under `docs/` and commit with:

   docs: <short summary>

2. Create a phase branch:

   git checkout -b phase-<number>-<short>

3. Implement code and tests. Run linters and `uv run pytest` locally.

4. Commit code changes with Conventional Commits (e.g. `feat:`)

5. Open a Pull Request against `main`. Ensure PR includes updated docs and passes CI.

6. Merge using `--no-ff` to preserve phase history:

   git checkout main
   git merge phase-4-editor --no-ff -m "Merge phase-4-editor: editor feature complete"

---

## Troubleshooting (common issues)

- Python version errors: install Python 3.14.2 and run `uv sync`
- Flet version mismatch: `uv add flet==0.28.3` and verify with `uv run python -c "import flet; print(flet.__version__)"`
- Missing dependencies: `uv sync`
- Corrupt JSON data: restore from backups in `data/backup/` or remove `data/prompts.json` and restart

---

## Where to get help

- Check `docs/` and `README.md`
- Open an Issue in the repository for workflow or documentation questions

---

**Last updated**: 2025-12-28
