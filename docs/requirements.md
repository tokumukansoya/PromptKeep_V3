# PromptKeep — Requirements (Flet)

> **AI Implementation Guide**: Use this document as the authoritative source for implementation decisions. If in doubt, check [`docs/ai_execution_guide.md`](PromptKeep_V3/docs/ai_execution_guide.md:1).

---

## Quick summary (essential for AI)

```yaml
Tech stack:
  Language: Python 3.14.2
  Framework: Flet 0.28.3
  Package manager: uv
  Persistence: JSON (local)

App:
  Type: Desktop app (cross-platform)
  Theme: Dark (fixed)
  Layout: Left sidebar + right card grid / editor view

Core features:
  - Prompt CRUD (create/read/update/delete)
  - Simple flat categories (single level)
  - Favorites
  - One-click copy
  - Trash with restore

Constraints:
  - Categories: single-level (flat)
  - Body preview: 40–80 characters
  - Card: square
  - Auto-save: debounce 2–3 seconds
  - Offline-first (local storage)
```

---

## 1. Purpose

Provide a simple desktop application for safely managing, viewing, editing, and copying prompts locally.

## 2. Scope

- Desktop app implemented with Flet, dark theme fixed.
- Local JSON persistence only. Cloud and import/export features are out of scope.
- Single-user.

## 3. Target users / use cases

- Individual users who create and organize prompts.
- Quickly copy frequently used prompts via card UI and edit when necessary.

## 4. Data model (local JSON)

- File path: `data/prompts.json` (auto-created if missing)
- Backup path: `data/backup/prompts_YYYYMMDD_HHMMSS.json`

JSON schema example:

```json
{
  "prompts": [
    {
      "id": "string (UUID v4)",
      "title": "string",
      "body": "string",
      "category_ids": ["cat_id_1"],
      "favorite": false,
      "deleted_at": null,
      "created_at": "ISO8601",
      "updated_at": "ISO8601"
    }
  ],
  "categories": [
    { "id": "string", "name": "string", "parent_id": null, "order": 0 }
  ],
  "trash": { "prompts": [], "categories": [] }
}
```

Data constraints:
- `category_ids` is ID-based (not names)
- `[]` indicates uncategorized
- `id` must be UUID v4
- `deleted_at`: null = active, ISO8601 = deleted

## 5. Functional requirements (priority)

Must (highest priority):
- Prompt CRUD with autosave and debounce (2–3s)
- Card UI: square cards (40–80 char preview)
- Flat categories (single level)
- Copy-to-clipboard
- Trash with restore

Should / Could: search & filters, performance optimizations

UI details and implementation specifics are given so AI can implement deterministically.

## 6. Non-functional requirements

- Performance: startup < 3s with 1k prompts; smooth scrolling; search < 100ms debounce result
- Reliability: atomic writes, backups, restore strategy
- Accessibility: keyboard navigation basics and WCAG contrasts
- Offline-first: no network required

## 7. UI / Component requirements

High-level component map: Sidebar, CardGrid, Editor view, Trash view, Snackbars, etc.

Refer to `docs/architecture.md` for component-level structure and `docs/coding_style.md` for implementation constraints.

## 8. State & Behavior

Use `AppState` dataclass to hold prompts, categories, trash IDs, selected category, query, view mode.
State changes should go through `StateManager` which handles debounce-saving and listener notifications.

## 9. Errors & exceptions

Use custom exceptions defined in `exceptions.py` (e.g., PromptNotFoundError, DataLoadError) and call `logger.error()` when errors occur.

## 10. Acceptance & validation

Provide machine-verifiable checks where possible (unit tests), plus manual validation steps in each Phase section. See `docs/ai_execution_guide.md` for phase-level checklists.

---

**Last updated**: 2025-12-28
