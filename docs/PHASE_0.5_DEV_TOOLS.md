# Phase 0.5: 開発ツール導入（Ruff + Loguru）

このPhaseは、Phase 0とPhase 1の間に実施する追加セットアップです。

---

## 目的
- Ruff（Linter/Formatter）の導入
- Loguru（ロギングライブラリ）の導入
- 既存コードの品質向上

---

## 実装内容

### 1. Ruffのインストールと設定

```bash
# 開発用パッケージとして追加
uv add --dev ruff

# VS Code拡張のインストール推奨
# charliermarsh.ruff
```

### 2. Loguruのインストール

```bash
# プロジェクト依存として追加
uv add loguru
```

### 3. utils/logger.py の作成

```python
"""ロギング設定（Loguru使用）

Loguruを使った統一的なロギング設定を提供する。
"""

import sys
from pathlib import Path
from loguru import logger

# デフォルト設定を削除
logger.remove()

# コンソール出力（開発時）
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG",
    colorize=True,
)

# ファイル出力
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logger.add(
    "logs/promptkeep_{time:YYYY-MM-DD}.log",
    rotation="00:00",  # 日次ローテーション
    retention="7 days",  # 7日間保持
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
)

# エラーログ専用
logger.add(
    "logs/error_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="30 days",  # 30日間保持
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}",
)

__all__ = ["logger"]
```

### 4. 既存コードの更新

#### 標準loggingからLoguruへの移行

**Before:**
```python
import logging

logger = logging.getLogger(__name__)
logger.info("メッセージ")
```

**After:**
```python
from loguru import logger

logger.info("メッセージ")
```

---

## 実装手順

### Step 1: Git ブランチ作成

```bash
git checkout main
git pull origin main
git checkout -b phase-0.5-dev-tools
```

### Step 2: パッケージインストール

```bash
# Ruff（開発用）
uv add --dev ruff

# Loguru
uv add loguru
```

### Step 3: utils/logger.py 作成

上記のコードを `utils/logger.py` に作成。

```bash
git add utils/logger.py pyproject.toml
git commit -m "feat: Phase 0.5 Loguru導入とlogger設定"
```

### Step 4: Ruff設定確認

`pyproject.toml` にRuff設定が追加されていることを確認。

```bash
git add pyproject.toml
git commit -m "chore: Phase 0.5 Ruff設定追加"
```

### Step 5: VS Code拡張インストール

VS Codeで以下の拡張をインストール：
- Ruff (charliermarsh.ruff)

`.vscode/settings.json` を作成：

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  },
  "ruff.lint.args": ["--config=pyproject.toml"],
  "ruff.format.args": ["--config=pyproject.toml"]
}
```

```bash
git add .vscode/settings.json
git commit -m "chore: Phase 0.5 VS Code設定追加"
```

### Step 6: 既存コードのフォーマット（任意）

```bash
# 全ファイルをフォーマット
uv run ruff format .

# Lintエラーを自動修正
uv run ruff check --fix .

git add .
git commit -m "style: Phase 0.5 Ruffでコードフォーマット"
```

### Step 7: 完了

```bash
git checkout main
git merge phase-0.5-dev-tools
git push origin main
git branch -d phase-0.5-dev-tools
```

---

## 検証可能な成功基準

### Ruff

```bash
# Lint チェック成功
uv run ruff check .
# → エラーなし、または軽微な警告のみ

# フォーマットチェック成功
uv run ruff format --check .
# → "All files left unchanged" と表示
```

### Loguru

```bash
# logger.py のインポート成功
uv run python -c "from utils.logger import logger; logger.info('Test')"
# → カラフルなログが出力される
# → logs/promptkeep_YYYY-MM-DD.log が作成される
```

### VS Code統合

- ファイル保存時に自動フォーマットされる
- Lintエラーが波線で表示される
- インポートが自動整理される

---

## ドキュメント更新

このPhaseは既存機能の改善なので、以下のドキュメントを更新：

1. ✅ `pyproject.toml` - Ruff/Loguru追加済み
2. ✅ `.clinerules` - Ruff/Loguru情報追加済み
3. ✅ `docs/TOOL_EVALUATION.md` - 評価レポート作成済み
4. ✅ `docs/QUICKSTART.md` - コマンド更新推奨

---

## 今後の使い方

### 日常的な使用

```bash
# コード書く → 保存（自動フォーマット）

# コミット前にチェック
uv run ruff check .
uv run ruff format --check .

# エラーがあれば自動修正
uv run ruff check --fix .
uv run ruff format .
```

### ログ確認

```bash
# 最新のログ確認
tail -f logs/promptkeep_$(date +%Y-%m-%d).log

# エラーログ確認
tail -f logs/error_$(date +%Y-%m-%d).log
```

---

## 依存関係

- **Phase 0**: 完了している必要がある
- **Phase 1以降**: このPhase完了後に実施

---

## 所要時間

- 実装: 15分
- 検証: 5分
- 合計: **20分**

---

**次のステップ**: [Phase 1: データ層の実装](implementation_plan.md#phase-1-データ層の実装必須)
