# AI Prompt Templates

> This file is a library of copy-paste-ready templates intended for use with AI tools (GitHub Copilot, Roo Code, etc.). Use `docs/ai_execution_guide.md` first for authoritative phase-level instructions.

This file is supportive: it provides concise templates that can be adapted and pasted into an AI agent for implementation tasks.

---

## Usage

Recommended flow for Roo Code or Copilot:

1. Read [`docs/ai_execution_guide.md`](PromptKeep_V3/docs/ai_execution_guide.md:1) — it contains detailed execution steps and checklists.
2. Find the relevant Phase section in this file and copy the template.
3. Replace any `[TODO]` placeholders with specifics for your task.
4. Paste into the AI and run.
5. Validate generated code using the checklists and tests; update docs if needed.

---

## Priority of references for AI

When executing with AI, follow this order:

1. [`docs/ai_execution_guide.md`](PromptKeep_V3/docs/ai_execution_guide.md:1) — primary execution guide
2. [`docs/coding_style.md`](PromptKeep_V3/docs/coding_style.md:1) — coding conventions
3. [`docs/requirements.md`](PromptKeep_V3/docs/requirements.md:1) — functional requirements
4. [`docs/architecture.md`](PromptKeep_V3/docs/architecture.md:1) — structure and responsibilities
5. [`docs/implementation_plan.md`](PromptKeep_V3/docs/implementation_plan.md:1) — roadmap
6. This file — templates for rapid iteration

---

## Template: Phase starter header (use at top of AI prompts)

```
[Phase X: Short title]

Environment:
- Python: 3.14.2
- Flet: 0.28.3
- Package manager: uv

Files:
- <list target files>

Requirements:
- <clear, actionable requirements>

Acceptance criteria:
- <checklist items>

Coding rules:
- Follow docs/coding_style.md
- Use Google-style docstrings and complete type hints

Testing:
- Add unit tests to PromptKeep_V3/tests/
- Ensure `uv run pytest` passes
```

---

## Example templates

### Phase 2-1: CategoryService implementation

```markdown
Phase 2-1: Implement CategoryService

Git:
```bash
git checkout main
git pull origin main
git checkout -b phase-2-1-category-service
```

Task:
- Implement category CRUD behavior as a service in `services/category_service.py`.

Requirements:
1. Create `CategoryService` class:
   - `__init__(self, data_service: DataService)`
   - `create_category(state, name) -> Category`
   - `update_category(state, category_id, name) -> Category`
   - `delete_category(state, category_id) -> None` (logical delete)
   - `get_category(state, category_id) -> Optional[Category]`
   - `list_categories(state, parent_id=None) -> List[Category]`
2. Flatter category policy: keep parent_id unused; categories are flat.
3. Use exceptions from `exceptions.py` and `logger.error()`.
4. Add unit tests under `PromptKeep_V3/tests/test_category_service.py`.

Verification:
- Unit tests pass locally
- Docstrings and type hints added
- Commit: `git commit -m "feat: Phase 2-1 CategoryService implementation"`
```
```

### Phase 2-3: ClipboardService

```markdown
Phase 2-3: Implement ClipboardService

Task:
- Implement `services/clipboard_service.py` to expose:
  - `copy_to_clipboard(page: ft.Page, text: str) -> bool`
  - `get_clipboard_text(page: ft.Page) -> Optional[str]`
- Use `page.set_clipboard()` and `page.get_clipboard()` (Flet API).
- Return boolean / None on failure and log errors.
- Add tests and docstrings.
```
```

### Phase 4-1: CardBody component

```markdown
Phase 4-1: Implement CardBody component

Task:
- Implement `ui/components/card/card_body.py`.
- Display title and a 40–80 character preview (use `utils.text_utils.create_preview`).
- Use `ui/styles` constants for typography and colors.
- Add a visual smoke test command (run the app) and unit tests if possible.
```
```

---

## AI usage tips

- Keep one Phase per prompt. Don't overload the AI with multiple Phases.
- Provide exact file paths and success-checklist.
- Ask AI to generate unit tests and run `uv run pytest` locally to validate.
- Require Google-style docstrings and full type hints in the prompt.
- If CI fails with a docs-first check, update `docs/` or `README.md` in the same branch and re-run.

---

## Practical examples and snippets

Include short snippets for common operations to help AI generate consistent code (examples below are intentionally concise):

- DataService save:
```python
def save_data(self, state: AppState) -> None:
    """Atomically write `state` to JSON with backup."""
    # use tempfile + os.replace for atomic write
```

- StateManager update:
```python
def update_prompts(self, prompts: list[Prompt]) -> None:
    self._state.prompts = prompts
    self._notify_listeners()
    self._schedule_save()
```

---

## Final notes

- Always validate AI-generated code with the checklists in `docs/ai_execution_guide.md`.
- Keep prompts focused, include tests in the same branch, and update documentation first (docs-first DDD).

---

Last updated: 2025-12-28
