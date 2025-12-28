# Flet 0.28.3 Feature Compatibility Checklist

Updated: 2025-12-27

This document summarizes which PromptKeep requirements are directly supported by Flet 0.28.3, and where workarounds are necessary.

---

## Fully supported features

- TextField (single-line and multi-line) — supports `min_lines`, `on_change`, `on_submit`.
- SnackBar — floating snackbars with `duration` control.
- Dropdown — flat list only; use visual indentation for pseudo-hierarchy.
- AlertDialog — modal dialogs available for confirmations and input.
- Clipboard API — `page.set_clipboard()` and `page.get_clipboard()` available.
- Keyboard events — `page.on_keyboard_event` and `KeyboardEvent` for key detection.
- GridView — `child_aspect_ratio=1.0` or `max_extent` to make square cards.

Workarounds noted where needed (e.g., for hierarchical dropdowns).

---

## Notes and recommendations

- For dropdown hierarchy: prefix option labels with indentation characters (e.g., "  ├") so the UI conveys hierarchy.
- For background tasks and debounced autosave, use `page.run_task()` (see `docs/ASYNC_GUIDELINES.md`).

---

**Last updated**: 2025-12-27
