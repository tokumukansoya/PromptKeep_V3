# PromptKeep - ツール・ライブラリ評価レポート

## 📋 提案されたツールの評価

### ✅ 導入推奨

#### 1. Ruff（VS Code拡張 + Pythonツール）
**用途**: Linter + Formatter

**メリット**:
- 高速（Rustベース）
- Black, isort, flake8の機能を統合
- 設定が簡単
- VS Code統合が優れている

**導入理由**:
- コード品質の自動チェック
- フォーマットの統一
- 開発効率の向上

**判定**: ✅ **導入**

---

#### 2. Loguru
**用途**: ロギング

**メリット**:
- 標準loggingより使いやすいAPI
- 自動的にカラフルな出力
- スタックトレースが見やすい
- 設定が簡単

**現状**: utils/logger.pyで標準loggingを使用

**導入理由**:
- デバッグ効率の向上
- より読みやすいログ出力
- エラートラブルシューティングが容易

**判定**: ✅ **導入（オプショナル）**

---

### ❌ 導入不要

#### 3. Pydantic
**用途**: データバリデーション

**評価**:
- 現在dataclassで十分機能している
- このアプリは外部API入力がない（ローカルJSON）
- オーバーエンジニアリングのリスク
- 学習コストが高い

**判定**: ❌ **不要**（シンプルさ優先）

---

#### 4. Flet-Easy / Flet-Router
**用途**: ルーティング・ナビゲーション

**評価**:
- このアプリは単一画面のビュー切り替え
- MainControllerで十分管理可能
- 複雑なルーティングは不要
- 追加の抽象化レイヤーは不要

**判定**: ❌ **不要**（現在の設計で十分）

---

#### 5. Filesystem MCP
**用途**: AIツール用ファイルシステムアクセス

**評価**:
- MCPはModel Context Protocol（AI連携用）
- このアプリはAI機能を持たない
- ローカルファイル操作は標準ライブラリで十分

**判定**: ❌ **不要**（スコープ外）

---

#### 6. Fetch / Web Search MCP
**用途**: AIツール用Web検索

**評価**:
- MCPはAI連携用
- このアプリは完全ローカル動作
- ネットワーク機能はスコープ外

**判定**: ❌ **不要**（スコープ外）

---

## 🎯 導入決定

### 即座に導入
1. ✅ **Ruff** - コード品質向上・必須
2. ✅ **Loguru** - 開発体験向上・推奨

### 導入しない
3. ❌ Pydantic - オーバーエンジニアリング
4. ❌ Flet-Easy/Router - 不要な複雑化
5. ❌ MCP系 - スコープ外

---

## 📦 導入による変更

### pyproject.toml
```toml
[project]
dependencies = [
    "flet==0.28.3",
    "loguru>=0.7.0",  # 新規追加
]

[project.optional-dependencies]
dev = [
    "ruff>=0.1.0",    # 新規追加
    "mypy>=1.0.0",
    "pytest>=7.0.0",
]

[tool.ruff]
line-length = 100
target-version = "py314"
select = ["E", "F", "I", "N", "W"]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### VS Code拡張
- Ruff (charliermarsh.ruff)

### utils/logger.py
```python
# 標準logging → Loguru に移行
from loguru import logger

# 設定はシンプルに
logger.add("logs/promptkeep.log", rotation="1 day")
```

---

## 🔄 移行計画

### Phase 0.5: ツール導入（新規Phase）
1. Ruffのインストール・設定
2. Loguruのインストール・設定
3. 既存コードのフォーマット
4. logger.pyの移行

**所要時間**: 30分
**優先度**: 高（早期導入推奨）

---

## 📝 今後の方針

### 追加を検討すべきタイミング

**Pydantic**:
- 外部APIとの連携が必要になった場合
- ユーザー入力の複雑なバリデーションが必要になった場合

**Flet-Easy/Router**:
- 画面数が5つ以上になった場合
- 複雑なナビゲーションが必要になった場合

**MCP系**:
- AI機能（プロンプト生成支援など）を追加する場合

---

**結論**: Ruff + Loguruのみ導入し、シンプルさを維持します。
