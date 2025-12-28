# PromptKeep — AI Execution Master Guide

This document is a complete execution guide for using AI tools (Roo Code, GitHub Copilot) to implement PromptKeep features autonomously or with human supervision.

---

## Principles: Document-Driven Development (DDD)

- Document-first: update specifications and documentation before implementing code.
- Every feature or behavior change must include a docs update (in `docs/` or `README.md`) and a `docs:` commit.
- Benefits: clear implementation targets for humans and AI, reduces divergence between code and spec.

Typical workflow:

```bash
# 1. Update docs and commit
git add docs/README.md docs/requirements.md
git commit -m "docs: describe X feature"

# 2. Implement code on a phase branch
git checkout -b phase-4-feature
# implement, run tests, commit
git commit -m "feat: implement X"
```

Refer to [`PromptKeep_V3/README.md`](PromptKeep_V3/README.md:1) and [`PromptKeep_V3/docs/CI.md`](PromptKeep_V3/docs/CI.md:1) for CI details and the docs-first check.

---

## How to use this file

For human developers:

1. Open the Phase section you want to implement.
2. Copy the "AI Execution Command" block and paste it into your AI tool or run manually.
3. Verify using the success checklist.

For AI (Roo Code / Copilot):

- Each Phase section contains a self-contained execution plan.
- When given an "AI Execution Command", perform the steps in order: create files, implement code following coding style, run tests, and perform the success checks.

---

## Prerequisites

- Python 3.14.2
- Flet 0.28.3
- Package manager: uv
- Repo root contains `PromptKeep_V3/` with `docs/`, `services/`, `ui/`, `models/`.
- Required docs present: [`docs/requirements.md`](PromptKeep_V3/docs/requirements.md:1), [`docs/architecture.md`](PromptKeep_V3/docs/architecture.md:1), [`docs/coding_style.md`](PromptKeep_V3/docs/coding_style.md:1), [`docs/implementation_plan.md`](PromptKeep_V3/docs/implementation_plan.md:1)

---

## CI and Docs-First enforcement

CI (GitHub Actions) runs on `push` and `pull_request` for `main` and `phase-*` branches and includes a lightweight "docs-first" check: if code under `PromptKeep_V3/` changes without `docs/` or `README.md` updates, CI can warn or fail. See [`PromptKeep_V3/docs/CI.md`](PromptKeep_V3/docs/CI.md:1) and the workflow template at `.github/workflows/ci.yml`.

When using AI to implement a Phase, ensure the related docs were updated and committed in the same branch before requesting the AI to implement code.

---

## Phase Map (high level)

- Phase 0: Base setup (complete)
- Phase 1: Data models (complete)
- Phase 2: Business logic (services)
  - 2-1: CategoryService
  - 2-2: Undo policy (trash/restore)
  - 2-3: ClipboardService
  - 2-4: SearchService
- Phase 3: UI style definitions (complete)
- Phase 4: Core UI components (cards, grid, snackbar)
- Phase 5: Editor and auto-save
- Phase 6: Sidebar & Category management
- Phase 7: Main view integration
- Phase 8–12: Trash, keyboard, search, error handling, tests

---

## Example: Phase 2-1 — CategoryService (AI Execution)

AI Execution Command (copy-paste to AI agent):

```markdown
PromptKeep — Phase 2-1: Implement CategoryService

Git steps (start a phase branch):
```bash
git checkout main
git pull origin main
git checkout -b phase-2-1-category-service
```

Task summary:
- Implement category CRUD operations as a service under `services/category_service.py`.
- Follow the project coding style and type hints.

Target file:
- `PromptKeep_V3/services/category_service.py`

Requirements:
1. Create `CategoryService` with dependency on `DataService`.
2. Implement methods:
   - create_category(state, name, parent_id=None) -> Category
   - update_category(state, category_id, name) -> Category
   - delete_category(state, category_id) -> None  (logical delete)
   - get_category(state, category_id) -> Optional[Category]
   - list_categories(state, parent_id=None) -> List[Category]
   - can_move_to(...), validate_depth(...), get_category_path(...)
3. Use exceptions from `exceptions.py` and `logger` for errors.
4. Add Google-style docstrings and full type hints.

Tests & verification:
- Add unit tests under `PromptKeep_V3/tests/test_category_service.py` covering CRUD.
- Run `uv run python -m pytest -q` and ensure tests pass.

Commit when done:
```bash
git add services/category_service.py tests/test_category_service.py
git commit -m "feat: Phase 2-1 CategoryService implementation"
```

Success checklist:
- [ ] `services/category_service.py` exists
- [ ] All methods implemented with type hints and docstrings
- [ ] Unit tests added and pass
- [ ] Errors logged with `logger.error()`
- [ ] Docs updated if any behavior or public API changed
```
```

---

## Example: Phase 4-1 — CardBody (AI Execution)

AI Execution Command (copy-paste):

```markdown
PromptKeep — Phase 4-1: Implement CardBody

Git steps:
```bash
git checkout main
git pull origin main
git checkout -b phase-4-1-card-body
```

Task summary:
- Implement UI component `PromptKeep_V3/ui/components/card/card_body.py` using Flet.
- Display title and preview (40–80 chars), apply style constants from `ui/styles`.

Verification:
- Visual smoke test by running `uv run python main.py`.
- Unit / component tests where applicable.

Commit:
```bash
git add ui/components/card/card_body.py
git commit -m "feat: Phase 4-1 CardBody component"
```

Success checklist:
- [ ] `ui/components/card/card_body.py` exists
- [ ] Title and preview shown with correct styles
- [ ] Type hints and docstrings present
```
```

---

## AI usage recommendations

- Provide the AI with exact file paths, coding style references, and success checklists.
- Keep each AI task focused (one Phase or subtask per prompt).
- Always review AI output and run tests locally.
- Update docs when the AI introduces new public behavior.

---

## Troubleshooting

- If CI fails with docs-first error: ensure docs/ or README.md were updated in the same branch.
- If tests fail: run `uv run python -m pytest -q` locally and inspect failures.
- If Flet API errors occur: confirm Flet version `0.28.3` is installed via `uv add flet==0.28.3`.

---

## Change log

- 2025-12-27: English translation and CI integration added.

---

**Note:** This file is intended to be authoritative for AI-driven implementation. Update it first when adding new Phases.
