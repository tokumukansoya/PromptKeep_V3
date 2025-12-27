# PromptKeep 開発者ガイド（人間向け）

> **5分で読める開発者向け必読ガイド**

このドキュメントは、PromptKeepプロジェクトに参加する**人間の開発者**が最低限読むべき内容をまとめたものです。

---

## 📌 このプロジェクトは何？

**PromptKeep** = プロンプト管理デスクトップアプリ（Flet製）

```
主な機能:
・プロンプトをカード形式で表示・管理
・カテゴリ階層（最大3階層）で整理
・ワンクリックでコピー
・お気に入り機能
・ゴミ箱・アンドゥ対応
```

---

## 🛠️ 技術スタック

| 項目 | 技術 |
|------|------|
| 言語 | Python 3.14.2 |
| UIフレームワーク | Flet 0.28.3 |
| パッケージ管理 | **uv**（pipは使わない） |
| データ保存 | ローカルJSON |
| テーマ | ダークテーマ固定 |

---

## 🚀 セットアップ手順

```bash
# 1. リポジトリをクローン
git clone <repo-url>
cd PromptKeep_V3

# 2. uv でセットアップ
uv sync

# 3. 実行
uv run python main.py
```

---

## 📂 プロジェクト構造（覚えるべき5つ）

```
PromptKeep_V3/
├── main.py           # エントリーポイント
├── models/           # データ構造（Prompt, Category）
├── services/         # ビジネスロジック
├── ui/               # UIコンポーネント
└── docs/             # ドキュメント
```

詳細は [architecture.md](architecture.md) を参照。

---

## 📝 開発ルール（3つだけ覚える）

### ルール1: ドキュメントファースト
```
仕様変更時:
1. ドキュメントを先に更新
2. Gitコミット (docs: ...)
3. コードを実装
4. Gitコミット (feat/fix: ...)
```

### ルール2: uvを使う
```bash
# パッケージ追加
uv add <package>

# 実行
uv run python main.py

# ❌ pipは使わない
```

### ルール3: Gitコミットメッセージ
```
<type>: <概要>

タイプ: feat / fix / docs / refactor / test / chore
例: feat: カード表示機能を実装
```

---

## 📖 ドキュメント参照ガイド

### 🔴 必読（これだけは読む）
| ドキュメント | 内容 | 行数 |
|-------------|------|------|
| **このファイル** | 人間向けクイックスタート | 〜100 |
| [architecture.md](architecture.md) | 設計・構造 | 377 |
| [coding_style.md](coding_style.md) | コーディング規約 | 567 |

### 🟡 必要に応じて
| ドキュメント | 内容 | いつ読む？ |
|-------------|------|-----------|
| [requirements.md](requirements.md) | 機能要件の詳細 | 仕様確認時 |
| [implementation_plan.md](implementation_plan.md) | Phase別計画 | 進捗確認時 |
| [git_workflow.md](git_workflow.md) | Git運用詳細 | ブランチ操作時 |

### 🔵 AI専用（人間は読まなくてOK）
| ドキュメント | 内容 |
|-------------|------|
| [ai_execution_guide.md](ai_execution_guide.md) | AI向け実装コマンド |
| [ai_prompts.md](ai_prompts.md) | AI向けプロンプト集 |

### � 技術参考
| ドキュメント | 内容 | いつ読む？ |
|-------------|------|-----------|
| [ASYNC_GUIDELINES.md](ASYNC_GUIDELINES.md) | 非同期処理ガイド | async/await使用時 |
| [FLET_FEATURE_COMPATIBILITY.md](FLET_FEATURE_COMPATIBILITY.md) | Flet機能検証結果 | UI実装で迷った時 |
| [PHASE_0.5_DEV_TOOLS.md](PHASE_0.5_DEV_TOOLS.md) | 開発ツール設定 | 環境構築時 |

### 📦 アーカイブ（過去の調査記録）
`docs/archive/` に移動済み（通常は参照不要）

---

## ⚠️ 重要な設計決定（これだけ覚える）

### 1. StateManager パターン
```python
# すべての状態変更は StateManager を経由
state_manager.update_prompts(prompts)  # ✅
self._state.prompts = prompts  # ❌ 直接変更禁止
```

### 2. category_ids はIDベース
```python
# カテゴリ名変更時もプロンプトに影響なし
prompt.category_ids = ["uuid-1", "uuid-2"]  # ✅ IDで参照
prompt.category_path = ["仕事", "AI"]  # ❌ 名前で参照しない
```

### 3. 非同期処理は page.run_task()
```python
# Flet推奨パターン
self._page.run_task(self._debounced_save)  # ✅
asyncio.create_task(...)  # ❌ 直接使用しない
```

### 4. カテゴリは最大3階層
```
✅ ルート > 子 > 孫
❌ ルート > 子 > 孫 > ひ孫（4階層は禁止）
```

---

## 🎯 Phase進捗

```
Phase 0   : ✅ プロジェクト初期化
Phase 0.5 : 🔄 開発ツールセットアップ
Phase 1   : ⬜ データモデル層
Phase 2   : ⬜ ビジネスロジック層
Phase 3   : ⬜ UIスタイル定義
...
Phase 12  : ⬜ 統合テスト
```

詳細は [implementation_plan.md](implementation_plan.md) を参照。

---

## ❓ よくある質問

**Q: Roo Code/Copilotで開発する場合は？**
A: [ai_execution_guide.md](ai_execution_guide.md) をAIに渡してください。

**Q: 新しいコンポーネントはどこに作る？**
A: `ui/components/` 配下。詳細は [architecture.md](architecture.md)。

**Q: テストはどう書く？**
A: `tests/` 配下に pytest で作成。詳細は [coding_style.md](coding_style.md)。

**Q: データ構造を確認したい**
A: [requirements.md](requirements.md) の「4. データモデル」セクション。

---

## 📚 外部リソース

- [Flet公式ドキュメント](https://flet.dev/docs/)
- [uv公式ドキュメント](https://docs.astral.sh/uv/)
- [Python型ヒント](https://docs.python.org/ja/3/library/typing.html)

---

**最終更新**: 2025-12-27
