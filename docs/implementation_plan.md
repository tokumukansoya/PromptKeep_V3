# PromptKeep 実装計画（ロードマップ）

> **AI実装者向け**: 各Phaseの詳細な実行コマンドは [ai_execution_guide.md](ai_execution_guide.md) を参照してください。このドキュメントは全体像を把握するためのマップです。

---

## 概要
このドキュメントは、PromptKeep を段階的に実装するための計画です。
各 Phase で実装する機能、依存関係、優先度、**検証可能な成功基準**を定義しています。

---

## Phase 0: 基盤セットアップ（必須・準備段階）

**目的**: 開発環境の整備とスケルトンコード生成

**実装内容**:
1. `requirements.txt` に依存パッケージを記載
2. `config.py` にアプリケーション設定定数を定義
3. ディレクトリ構造の自動生成
4. `main.py` のスケルトン作成
5. `utils/` 内のヘルパー関数スタブ作成

**成果物**:
- requirements.txt（Flet 0.28.3 固定）
- config.py（定数管理）
- ディレクトリツリー
- main.py（エントリーポイント）
- utils/*.py（スタブ）

**検証可能な成功基準**:
```bash
# 1. uvのインストール確認
uv --version
# → uv 0.x.x が表示される

# 2. 依存関係のインストール成功
uv sync
# → エラーなく完了

# 2. config.py の定数確認
python -c "from config import MAX_CATEGORY_DEPTH; print(MAX_CATEGORY_DEPTH)"
# → 3 が出力される

# 3. ディレクトリ構造確認
ls -R
# → models/, services/, ui/, utils/, data/ が存在する

# 4. main.py の実行確認
uv run python main.py
# → エラーなく起動（UI表示はまだ空でOK）
```

**依存**: なし
**難易度**: ⭐
**予想時間**: 30分

---

## Phase 0.5: 開発ツール導入（推奨）

**目的**: RuffとLoguruの導入で開発効率向上

**実装内容**:
1. Ruff（Linter/Formatter）のインストールと設定
2. Loguru（ロギング）のインストール
3. `utils/logger.py` の作成
4. VS Code設定ファイルの作成

**成果物**:
- Ruffが使える状態
- Loguruによる統一ロギング
- 保存時自動フォーマット

**検証可能な成功基準**:
```bash
# Ruffが動作する
uv run ruff check .
uv run ruff format --check .

# Loguruが動作する
uv run python -c "from utils.logger import logger; logger.info('Test')"
# → カラフルなログが出力される
# → logs/promptkeep_YYYY-MM-DD.log が作成される
```

**詳細**: [docs/PHASE_0.5_DEV_TOOLS.md](PHASE_0.5_DEV_TOOLS.md)

**依存**: Phase 0
**難易度**: ⭐
**予想時間**: 20分

---

## Phase 1: データ層の実装（必須）

**目的**: プロンプト・カテゴリのデータモデルとスキーマを確定

**実装内容**:
1. `models/prompt.py` - Prompt データクラス定義
2. `models/category.py` - Category データクラス定義
3. `models/app_state.py` - AppState（全体状態管理）
4. `services/data_service.py` - JSON ファイルの読み書き（基本実装）
5. `utils/file_utils.py` - ファイル操作ユーティリティ
6. `utils/date_utils.py` - 日時ユーティリティ
7. `utils/text_utils.py` - テキスト処理（プレビュー生成など）
8. `exceptions.py` - カスタム例外クラス

**成果物**:
- Prompt/Category/AppState のデータクラス
- JSON スキーマに対応した読み書き
- バックアップ機能の基本構造

**検証可能な成功基準**:
```python
# 1. データクラスのインポート成功
from models.prompt import Prompt
from models.category import Category
from models.app_state import AppState
# → エラーなし

# 2. Promptオブジェクトの作成
from datetime import datetime
p = Prompt(
    id="test-id",
    title="テスト",
    body="本文",
    category_ids=[],
    favorite=False,
    deleted_at=None,
    created_at=datetime.now(),
    updated_at=datetime.now()
)
print(p.title)
# → "テスト" が出力される

# 3. DataServiceのJSON読み書き
from services.data_service import DataService
ds = DataService("data/test.json")
state = AppState(prompts=[p], categories=[], trash_prompt_ids=[], trash_category_ids=[])
ds.save(state)
# → data/test.json が作成される

loaded_state = ds.load()
print(len(loaded_state.prompts))
# → 1 が出力される

# 4. text_utils のプレビュー生成
from utils.text_utils import create_preview
preview = create_preview("これは長いテキストです。" * 10, max_length=50)
print(len(preview))
# → 50前後（省略記号含む）

# 5. 日時フォーマット
from utils.date_utils import format_datetime
formatted = format_datetime(datetime.now())
print(formatted)
# → "2025-12-27 12:34:56" 形式で出力
```

**依存**: Phase 0
**難易度**: ⭐⭐
**予想時間**: 1.5時間

**実装順序**:
1. models/prompt.py
2. models/category.py
3. models/app_state.py
4. exceptions.py
5. utils/file_utils.py, date_utils.py, text_utils.py
6. services/data_service.py（読み込み）
7. services/data_service.py（書き込み・バックアップ）

---

## Phase 2: ビジネスロジック層（必須）

**目的**: プロンプト・カテゴリの CRUD 操作と状態管理を実装

**実装内容**:
1. **`services/state_manager.py`** - **状態管理の中核（最優先）**
   - StateManagerクラスの実装
   - デバウンス付き自動保存
   - リスナーパターンによる通知機能
2. `services/prompt_service.py` - プロンプトビジネスロジック
   - `create_prompt()` - Promptオブジェクト生成のみ
   - 状態変更はStateManagerに委譲
3. `services/category_service.py` - カテゴリビジネスロジック（シンプル）
   - `create_category()` - Categoryオブジェクト生成（parent_idなし）
   - `update_category()` - 名前更新
   - `delete_category()` - 削除
4. `services/clipboard_service.py` - クリップボード操作
   - `copy_to_clipboard()`
5. `services/search_service.py` - 検索・フィルタ
   - `search_prompts()`, `filter_by_category()`
   - `filter_by_favorite()`

**Note**: アンドゥはCtrl+Zのキー操作で直前状態を戻す機能ではなく、削除はゴミ箱へ移動し、UIの「復元」操作で対応します。独立した `UndoService` の実装は必須ではありません。

**成果物**:
- StateManager（状態管理の中核）
- 各Serviceのビジネスロジック（状態変更なし、純粋関数）
- UIなしで動作確認可能

**検証可能な成功基準**:
```python
# 1. StateManagerの動作確認
from services.state_manager import StateManager
from services.data_service import DataService

ds = DataService("data/test.json")
sm = StateManager(ds, debounce_seconds=0.5)

# リスナー登録
def on_state_change(state):
    print(f"State updated: {len(state.prompts)} prompts")

sm.add_listener(on_state_change)

# 状態変更
sm.load()  # → ファイルから読み込み
prompt = Prompt.create("Test", "Body", [])
sm.update_prompts([prompt])  # → リスナー通知 + 0.5秒後に自動保存

# 2. PromptServiceのビジネスロジック
from services.prompt_service import PromptService

ps = PromptService()

# プロンプト作成（オブジェクト生成のみ）
prompt = ps.create_prompt("タイトル", "本文", [])
print(prompt.id)  # → UUID が出力される

# カテゴリ深度検証
assert ps.validate_category_depth(["cat1", "cat2", "cat3"]) == True
assert ps.validate_category_depth(["cat1", "cat2", "cat3", "cat4"]) == False

# 3. CategoryServiceの階層パス生成
from services.category_service import CategoryService

cs = CategoryService()

categories = [
    Category(id="cat1", name="親", order=0),
    Category(id="cat2", name="子", order=0),
    Category(id="cat3", name="孫", order=0),
]

# カテゴリはフラット（階層なし）
print([c.name for c in categories])  # → ["親", "子", "孫"]

# 階層エラーの概念はないため検証不要

# 4. SearchService
from services.search_service import SearchService

ss = SearchService()
prompts = [
    Prompt.create("Python入門", "Pythonの基礎", []),
    Prompt.create("JavaScript入門", "JSの基礎", []),
]

results = ss.search_prompts(prompts, "python")
print(len(results))  # → 1（大文字小文字を区別しない）
print(results[0].title)  # → "Python入門"
```

**依存**: Phase 1
**難易度**: ⭐⭐⭐
**予想時間**: 2.5時間

**実装順序**:
1. **services/state_manager.py**（最優先・他の全てがこれに依存）
2. services/prompt_service.py（ビジネスロジックのみ）
3. services/category_service.py（階層検証・パス生成）
4. services/undo_service.py
5. services/clipboard_service.py
6. services/search_service.py

---

## Phase 3: UI スタイル定義（必須）

**目的**: デザイン定数を一元管理し、UI の基本となるスタイル定義

**実装内容**:
1. `ui/styles/colors.py` - カラーパレット（ダークテーマ）
2. `ui/styles/typography.py` - フォント・テキストサイズ
3. `ui/styles/spacing.py` - 余白・パディング・マージン
4. `ui/styles/card_style.py` - カードのスタイル定義

**成果物**:
- スタイル定数の完全セット
- カード形状（正方形）の定義

**依存**: Phase 0
**難易度**: ⭐
**予想時間**: 30分

---

## Phase 4: UI コアコンポーネント（必須）

**目的**: カード表示とグリッドレイアウトの実装

**実装内容**:
1. `ui/components/card/card_body.py` - カード本文（タイトル + プレビュー）
2. `ui/components/card/card_header.py` - カードヘッダー（コピーボタン、お気に入り）
3. `ui/components/card/prompt_card.py` - カード全体の組立
4. `ui/views/card_grid_view.py` - カードグリッド表示
5. `ui/components/common/snackbar.py` - トースト通知

**成果物**:
- 正方形カードのプレビュー表示（操作不可）
- グリッドレイアウト（レスポンシブ）

**依存**: Phase 2, Phase 3
**難易度**: ⭐⭐⭐
**予想時間**: 2時間

**実装順序**:
1. ui/styles/ ← 先に完成させる
2. ui/components/card/card_body.py
3. ui/components/card/card_header.py
4. ui/components/card/prompt_card.py
5. ui/views/card_grid_view.py
6. ui/components/common/snackbar.py

---

## Phase 5: 編集機能（必須）

**目的**: プロンプトの新規作成・編集機能を実装

**実装内容**:
1. `ui/components/editor/title_field.py` - タイトル入力
2. `ui/components/editor/body_field.py` - 本文テキストエリア
3. `ui/components/editor/category_selector.py` - カテゴリ選択
4. `ui/components/editor/editor_toolbar.py` - ツールバー（戻るボタン）
5. `ui/views/edit_view.py` - 編集ビュー全体
6. `ui/controllers/edit_controller.py` - 編集操作のコントローラー
7. 自動保存機能（デバウンス付き）

**成果物**:
- プロンプトの新規作成・編集が可能
- 自動保存機能の動作

**依存**: Phase 2, Phase 4
**難易度**: ⭐⭐⭐
**予想時間**: 2.5時間

**実装順序**:
1. ui/components/editor/title_field.py
2. ui/components/editor/body_field.py
3. ui/components/editor/category_selector.py（シンプル版）
4. ui/components/editor/editor_toolbar.py
5. ui/views/edit_view.py
6. ui/controllers/edit_controller.py
7. 自動保存ロジック追加

---

## Phase 6: サイドバー - カテゴリ管理（重要）

**目的**: カテゴリの表示・追加・編集（フラットな1階層）

**実装内容**:
1. `ui/components/sidebar/search_box.py` - 検索ボックス
2. `ui/components/sidebar/category_item.py` - カテゴリアイテム（シンプル表示）
3. `ui/components/sidebar/category_list.py` - カテゴリ一覧表示（フラット）
4. `ui/components/dialogs/add_category_dialog.py` - カテゴリ追加ダイアログ
5. `ui/components/sidebar/add_category_button.py` - カテゴリ追加ボタン
6. `ui/components/sidebar/sidebar.py` - サイドバー全体
7. `ui/controllers/category_controller.py` - カテゴリ操作

**成果物**:
- サイドバーの完全実装
- ドラッグ&ドロップは実装しない（フラットなカテゴリ管理）
- カテゴリ選択によるフィルタリング

**依存**: Phase 2, Phase 4, Phase 5
**難易度**: ⭐⭐
**予想時間**: 1.5時間

**実装順序**:
1. ui/components/sidebar/search_box.py
2. ui/components/dialogs/add_category_dialog.py
3. ui/components/sidebar/add_category_button.py
4. ui/components/sidebar/category_item.py
5. ui/components/sidebar/category_list.py
6. ui/components/sidebar/sidebar.py
7. ui/controllers/category_controller.py

---

## Phase 7: メイン画面統合（必須）

**目的**: 全コンポーネントを統合し、メイン画面を完成

**実装内容**:
1. `ui/app.py` - Flet アプリケーションクラス
2. `ui/views/main_view.py` - メイン画面レイアウト
3. `ui/controllers/main_controller.py` - メイン画面のコントローラー
4. `main.py` - エントリーポイントの完成

**成果物**:
- 左サイドバー + 右カードグリッド + 編集ビューの統合
- 全体的なナビゲーション

**依存**: Phase 4, Phase 5, Phase 6
**難易度**: ⭐⭐⭐
**予想時間**: 2時間

---

## Phase 8: ゴミ箱機能（重要）

**目的**: 削除データの管理と復元機能

**実装内容**:
1. `ui/views/trash_view.py` - ゴミ箱ビュー
2. `ui/controllers/trash_controller.py` - ゴミ箱操作
3. ゴミ箱を空にする機能
4. 復元ボタンの実装

**成果物**:
- ゴミ箱画面（削除済みプロンプト一覧）
- 復元・完全削除機能

**依存**: Phase 2, Phase 7
**難易度**: ⭐⭐
**予想時間**: 1.5時間

---

## Phase 9: キーボード操作（重要）

**目的**: キーボードショートカット実装（コピーなど）

**実装内容**:
1. `ui/controllers/keyboard_controller.py` - キーボード操作の一元管理
   - Ctrl+C：コピー（コンテキスト依存）
   - Ctrl+F：検索フォーカス（任意）
   - その他ショートカット

**成果物**:
- キーボードショートカットの動作（Ctrl+ZによるUndoは実装対象外）

**依存**: Phase 2, Phase 7
**難易度**: ⭐⭐
**予想時間**: 1時間

---

## Phase 10: 検索・フィルタ機能（低優先）

**目的**: タイトル・本文全文検索とフィルタ

**実装内容**:
1. 検索ボックスの入力ハンドリング
2. リアルタイム検索（デバウンス付き）
3. カテゴリフィルタとの AND 結合

**成果物**:
- 検索・フィルタの完全動作

**依存**: Phase 2, Phase 6
**難易度**: ⭐⭐
**予想時間**: 1時間

---

## Phase 11: エラーハンドリング・ロギング（重要）

**目的**: 堅牢性の向上

**実装内容**:
1. 全レイヤーの例外ハンドリング強化
2. ロギング設定の確認
3. バックアップ・リカバリ機能の確認

**成果物**:
- エラーメッセージの適切な表示
- ログ出力の確認

**依存**: Phase 2, Phase 7
**難易度**: ⭐⭐
**予想時間**: 1時間

---

## Phase 12: Undo機能拡張（オプション・低優先度）

**目的**: Undo機能の拡張は今回のスコープ外（ゴミ箱復元で対応）

**実装内容**:
1. 現時点では追加のUndo/Redoは計画しない
2. 将来的に要望が出た場合は Commandパターンで検討

**Note**:
- 削除の復元はゴミ箱の「復元」操作で対応する

**依存**: なし
**難易度**: ⭐
**予想時間**: 0.5時間

---

## Phase 13: テスト・バグ修正（重要）

**目的**: 機能的な完成と品質向上

**実装内容**:
1. 統合テスト（手動）
2. エッジケースの確認
3. UI/UX の微調整
4. パフォーマンスチューニング（1000件超のテスト）
5. ページネーション動作確認

**成果物**:
- 安定して動作するアプリケーション

**依存**: すべて
**難易度**: ⭐⭐⭐
**予想時間**: 2時間

---

## 依存関係図

```
Phase 0 (基盤)
  ├─→ Phase 0.5 (開発ツール) ★ 新規
  │    └─→ Phase 1 (データ層)
  │         ├─→ Phase 2 (ビジネスロジック)
  │    ├─→ Phase 2 (ビジネスロジック)
  │    │    ├─→ Phase 5 (編集機能)
  │    │    ├─→ Phase 6 (カテゴリ管理)
  │    │    └─→ Phase 8 (ゴミ箱)
  │    └─→ Phase 3 (スタイル)
  │
  ├─→ Phase 3 (スタイル)
  │    └─→ Phase 4 (コアコンポーネント)
  │         ├─→ Phase 5 (編集機能)
  │         ├─→ Phase 6 (カテゴリ管理)
  │         └─→ Phase 7 (メイン統合)
  │
  └─→ Phase 4 (コアコンポーネント)
       ├─→ Phase 5 (編集機能)
       ├─→ Phase 6 (カテゴリ管理)
       └─→ Phase 7 (メイン統合)
            ├─→ Phase 8 (ゴミ箱)
            ├─→ Phase 9 (キーボード操作)
            ├─→ Phase 10 (検索)
            └─→ Phase 11 (エラーハンドリング)
                 └─→ Phase 12 (テスト)
```

---

## マイルストーン

| Milestone | 目安フェーズ | 達成時の状態 |
|-----------|-----------|-----------|
| **M1: 起動可能** | Phase 0-1 | アプリが起動し、JSON の読み書きが動作 |
| **M2: カード表示** | Phase 4 | プロンプトがカード表示される |
| **M3: CRUD 機能** | Phase 5 | プロンプトの作成・編集・表示ができる |
| **M4: カテゴリ管理** | Phase 6 | カテゴリの作成・選択・階層化ができる |
| **M5: 完全統合** | Phase 7 | 全機能が連動して動作 |
| **M6: 補助機能** | Phase 8-10 | ゴミ箱、キーボード、検索が動作 |
| **M7: 安定運用** | Phase 11-12 | エラーハンドリング完備、テスト済み |

---

## 並列実装可能な Phase

以下の Phase は並列に実装可能（依存がない）：

- **Phase 0 と Phase 3** は同時実装可能
- Phase 1 の完成後、Phase 2 と Phase 3 は並列可能
- Phase 4 と Phase 2 は並列可能（ただし統合は Phase 4 後）

---

## 推奨実装順序（実際のステップ）

1. **Phase 0** : 環境セットアップ
2. **Phase 1** : データモデル定義
3. **Phase 3** : スタイル定義（Phase 1 と並列可）
4. **Phase 2** : ビジネスロジック実装
5. **Phase 4** : カード表示
6. **Phase 5** : 編集機能
7. **Phase 6** : サイドバー
8. **Phase 7** : メイン統合
9. **Phase 8** : ゴミ箱
10. **Phase 9** : キーボード操作
11. **Phase 10** : 検索（低優先のため後回し可）
12. **Phase 11** : エラーハンドリング
13. **Phase 12** : テスト・最適化

---

## AI への指示ガイドライン

各 Phase を AI に指示する際は、以下の形式で指示してください：

```
【Phase X: [フェーズ名] 実装】

対象ファイル：
- models/xxx.py
- services/xxx.py
- ...

要件：
- [実装内容]

依存：Phase Y の完成を前提
規約：docs/coding_style.md に準拠

参考：
- アーキテクチャ: docs/architecture.md
- 要件定義: docs/requirements.md
- コーディング規約: docs/coding_style.md
```

---

## 進捗管理

各 Phase 完了時に、以下をチェック：

- [ ] すべてのファイルが作成された
- [ ] コーディング規約に準拠している
- [ ] 型ヒント・Docstring が完全
- [ ] エラーハンドリングが適切
- [ ] テスト可能な実装（テストコードなくても動作確認可能か）
- [ ] 次 Phase への依存が満たされているか
