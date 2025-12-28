# PromptKeep Coding Style Guide

## Environment & versions (strict)

- Python: 3.14.2+ (project uses 3.14.2)
- Flet: 0.28.3 (do not instruct AI to use other versions)
- See `requirements.txt` for other dependencies

Important: When instructing AI, always state versions explicitly, e.g. “Use Flet 0.28.3” or “Target Python 3.14.2”.

---

## 1. File layout

### 1.1 File header
Every Python module must start with a concise module docstring:

```python
"""One-line module summary.

Longer description if needed.

Attributes:
    CONSTANT_NAME: description

Note:
    Implementations should be compatible with Flet 0.28.3.
"""

# imports...
```

### 1.2 Import ordering

Follow: standard library → third-party → local

```python
# Standard
import json
from typing import List, Optional

# Third-party
import flet as ft

# Local
from models.prompt import Prompt
from services.data_service import DataService
```

Rules:
- One blank line between groups
- Alphabetical order inside each group is preferred
- Mixing `import X` and `from X import Y` is OK

### 1.3 File length
No strict limit; consider splitting modules > 500 lines.

---

## 2. Type hints (mandatory)

All functions must include complete type annotations for arguments and return values.

Good examples:

```python
def create_prompt(
    title: str,
    body: str,
    category_ids: list[str]
) -> Prompt:
    """Create a prompt object."""
    ...
```

Use Optional, Union, Dict, List from typing when appropriate and prefer explicit typing.

Recommended tools: mypy for static type checking. Instruct AI: "Produce code that passes mypy checks." 

---

## 3. Docstrings (Google style)

- All public functions and classes must have Google-style docstrings.
- Example:

```python
def update_prompt(prompt_id: str, title: Optional[str] = None) -> Prompt:
    """Update an existing prompt.

    Args:
        prompt_id: Target prompt ID.
        title: New title; if omitted, title is unchanged.

    Returns:
        Updated prompt.

    Raises:
        ValueError: If prompt_id not found.
    """
```

Module docstrings should appear at the top of the file.

---

## 4. Error handling

- Use structured logging and meaningful exceptions.
- Example logging setup:

```python
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
```

- Use custom exceptions defined in `exceptions.py` and call `logger.error()` or `logger.exception()` when appropriate.

---

## 5. Constants

Place constants in logical files:
- Colors, typography, spacing: `ui/styles/*`
- App settings: `config.py`

Example `config.py` contains APP_VERSION, MIN_PYTHON_VERSION, PREVIEW_MAX_LENGTH, MAX_CATEGORY_DEPTH, etc.

---

## 6. Comment density

Rules:
- Docstrings required for public functions/classes
- Add inline comments only for non-obvious logic
- Avoid excessive comments that restate the code

---

## 7. Naming conventions

Follow PEP 8:
- Functions / methods: snake_case
- Variables: snake_case
- Constants: UPPER_SNAKE_CASE
- Classes: PascalCase
- Private: _prefix

Examples: `get_prompt`, `prompt_id`, `MAX_CATEGORY_DEPTH`, `PromptService`.

---

## 8. Design principles

- Dependency injection: inject services into consumers (no global singletons)
- State handled via `StateManager`
- Keep logic testable and side-effect free where possible

Example:

```python
class PromptService:
    def __init__(self, data_service: DataService) -> None:
        self.data_service = data_service
```

---

## 9. Flet compatibility

- Target Flet 0.28.3 APIs
- Do not use deprecated methods removed before 0.28.3
- When instructing AI: specify "Use Flet 0.28.3 API" and include examples or links if necessary

---

## 10. AI instruction template (recommended)

When instructing AI, include:

- Versions: Python 3.14.2, Flet 0.28.3
- Target file path(s)
- Clear requirements and acceptance criteria
- Coding rules to follow (this doc: `docs/coding_style.md`)
- Example snippet or test cases to validate against

Example prompt header:

```
[Python coding task]

Version:
- Python 3.14.2
- Flet 0.28.3

Files:
- services/category_service.py

Requirements:
- ...

Constraints:
- All functions must have type hints
- Docstrings must use Google style
- Use logger.error() for failures
```

---

## 11. Code review checklist (for AI output)

- [ ] Compatible with Python 3.14.2
- [ ] Compatible with Flet 0.28.3
- [ ] All functions have type hints
- [ ] Public functions/classes have Google-style docstrings
- [ ] Proper error handling and logging
- [ ] Constants are in `config.py` or `ui/styles/`
- [ ] Naming follows PEP 8
- [ ] Import order is correct
- [ ] No global singletons

---

## 12. References

- PEP 8: https://pep8.org/
- Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
- Flet docs: https://flet.dev/
- Python 3.14 docs: https://docs.python.org/3.14/

---

Last updated: 2025-12-28
