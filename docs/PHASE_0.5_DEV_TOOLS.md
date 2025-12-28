# Phase 0.5: Developer Tooling (Ruff + Loguru)

This Phase is an optional setup step between Phase 0 and Phase 1 to improve developer productivity and code quality.

---

## Goals

- Add Ruff (linter/formatter)
- Add Loguru for consistent logging
- Improve existing code quality and integrate tools into editor and CI

---

## Implementation

### 1. Install Ruff

```bash
# Add as a dev dependency
uv add --dev ruff
```

Recommend installing the VS Code extension: charliermarsh.ruff.

### 2. Install Loguru

```bash
uv add loguru
```

### 3. Create `utils/logger.py`

Provide a central logging configuration using Loguru.

```python
"""Logging setup (Loguru)

Provides consistent logging configuration for the project.
"""

import sys
from pathlib import Path
from loguru import logger

logger.remove()

# Console logger (development)
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG",
    colorize=True,
)

# File logger
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logger.add(
    "logs/promptkeep_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
)

# Error logger
logger.add(
    "logs/error_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="30 days",
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}",
)

__all__ = ["logger"]
```

### 4. Migrate from standard logging to Loguru (optional)

Before:

```python
import logging
logger = logging.getLogger(__name__)
logger.info("message")
```

After:

```python
from loguru import logger
logger.info("message")
```

---

## Steps

1. Create a branch:

```bash
git checkout main
git pull origin main
git checkout -b phase-0.5-dev-tools
```

2. Install packages:

```bash
uv add --dev ruff
uv add loguru
```

3. Add `utils/logger.py` and commit:

```bash
git add utils/logger.py pyproject.toml
git commit -m "feat: Phase 0.5 Add Loguru logger and Ruff config"
```

4. Configure VS Code settings for Ruff (create `.vscode/settings.json`) and commit.

5. Optionally run formatting and linting:

```bash
uv run ruff format .
uv run ruff check .
```

6. Merge back to main when ready.

---

## Validation

- Ruff check reports no blocking issues
- Logger import works:

```bash
uv run python -c "from utils.logger import logger; logger.info('test')"
```

- Log files are created under `logs/`

---

## Notes

- This Phase mainly improves developer experience and does not change runtime behavior of the app.
- Update `pyproject.toml` and `.clinerules` as needed.

---

**Last updated**: 2025-12-28
