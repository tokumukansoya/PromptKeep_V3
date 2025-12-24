# PromptKeep アーキテクチャ設計

## 1. ディレクトリ構造

```
PromptKeep_V3/
├── main.py                          # アプリケーションのエントリーポイント
├── requirements.txt                 # 依存パッケージ
├── .gitignore                       # Git除外設定
│
├── data/                            # データ永続化
│   ├── prompts.json                 # プロンプトデータ（自動生成）
│   └── backup/                      # バックアップファイル（自動生成）
│
├── docs/                            # ドキュメント
│   ├── requirements.md              # 要件定義
│   └── architecture.md              # アーキテクチャ設計（本ファイル）
│
├── models/                          # データモデル
│   ├── __init__.py
│   ├── prompt.py                    # Promptモデル（id, title, body, category_path, favorite, etc.）
│   ├── category.py                  # Categoryモデル（id, name, parent_id）
│   └── app_state.py                 # アプリ全体の状態管理
│
├── services/                        # ビジネスロジック層
│   ├── __init__.py
│   ├── data_service.py              # データ永続化サービス（JSON読み書き）
│   ├── prompt_service.py            # プロンプトCRUD操作
│   ├── category_service.py          # カテゴリCRUD操作
│   ├── search_service.py            # 検索・フィルタリングロジック
│   ├── clipboard_service.py         # クリップボード操作
│   └── undo_service.py              # アンドゥ・リドゥ管理
│
├── ui/                              # UI層
│   ├── __init__.py
│   │
│   ├── app.py                       # Fletアプリケーションのメインクラス
│   │
│   ├── views/                       # 画面・ビュー
│   │   ├── __init__.py
│   │   ├── main_view.py             # メイン画面全体のレイアウト
│   │   ├── card_grid_view.py        # カードグリッド表示エリア
│   │   ├── edit_view.py             # プロンプト編集ビュー
│   │   └── trash_view.py            # ゴミ箱ビュー
│   │
│   ├── components/                  # 再利用可能なUIコンポーネント
│   │   ├── __init__.py
│   │   │
│   │   ├── sidebar/                 # サイドバー関連
│   │   │   ├── __init__.py
│   │   │   ├── sidebar.py           # サイドバー全体
│   │   │   ├── search_box.py        # 検索ボックス
│   │   │   ├── category_tree.py     # カテゴリツリー
│   │   │   ├── category_item.py     # カテゴリアイテム（ドラッグ対応）
│   │   │   └── add_category_button.py  # カテゴリ追加ボタン
│   │   │
│   │   ├── card/                    # カード関連
│   │   │   ├── __init__.py
│   │   │   ├── prompt_card.py       # プロンプトカード全体
│   │   │   ├── card_header.py       # カードヘッダー（お気に入り、コピー）
│   │   │   ├── card_body.py         # カード本文（タイトル、プレビュー）
│   │   │   └── card_actions.py      # カードアクション（削除など）
│   │   │
│   │   ├── editor/                  # 編集エリア関連
│   │   │   ├── __init__.py
│   │   │   ├── title_field.py       # タイトル入力フィールド
│   │   │   ├── body_field.py        # 本文テキストエリア
│   │   │   ├── category_selector.py # カテゴリ選択UI
│   │   │   └── editor_toolbar.py    # エディタツールバー（戻るボタンなど）
│   │   │
│   │   ├── dialogs/                 # ダイアログ
│   │   │   ├── __init__.py
│   │   │   ├── add_category_dialog.py    # カテゴリ追加ダイアログ
│   │   │   └── confirmation_dialog.py    # 確認ダイアログ（汎用）
│   │   │
│   │   └── common/                  # 共通コンポーネント
│   │       ├── __init__.py
│   │       ├── snackbar.py          # スナックバー（通知）
│   │       ├── icon_button.py       # カスタムアイコンボタン
│   │       └── loading_indicator.py # ローディングインジケーター
│   │
│   ├── styles/                      # スタイル定義
│   │   ├── __init__.py
│   │   ├── colors.py                # カラーパレット（ダークテーマ）
│   │   ├── typography.py            # フォント、サイズ定義
│   │   ├── spacing.py               # 余白、パディング定数
│   │   └── card_style.py            # カードスタイル定義
│   │
│   └── controllers/                 # UIコントローラー（イベントハンドリング）
│       ├── __init__.py
│       ├── main_controller.py       # メイン画面のコントローラー
│       ├── card_controller.py       # カード操作のコントローラー
│       ├── edit_controller.py       # 編集操作のコントローラー
│       ├── category_controller.py   # カテゴリ操作のコントローラー
│       └── keyboard_controller.py   # キーボードショートカット管理
│
└── utils/                           # ユーティリティ
    ├── __init__.py
    ├── file_utils.py                # ファイル操作ユーティリティ
    ├── date_utils.py                # 日時フォーマット
    ├── text_utils.py                # テキスト処理（プレビュー生成など）
    ├── validation.py                # バリデーション
    └── logger.py                    # ロギング設定
```

## 2. 各層の責務

### models/
- **役割**: データ構造の定義。ビジネスロジックやUIには依存しない。
- **責務**:
  - Prompt/Category のデータクラス定義
  - アプリ全体の状態管理（AppState）
  - データの型定義とバリデーション

### services/
- **役割**: ビジネスロジックの実装。UIから独立して動作。
- **責務**:
  - データの CRUD 操作
  - JSONファイルの読み書き
  - 検索・フィルタリング
  - 削除のアンドゥ管理

### ui/views/
- **役割**: 画面全体のレイアウトと構成。
- **責務**:
  - メイン画面のレイアウト
  - カードグリッドの配置
  - 編集ビューの表示切り替え

### ui/components/
- **役割**: 再利用可能な UI パーツ。単一の責任を持つ小さなコンポーネント。
- **責務**:
  - 各コンポーネントは独立してテスト可能
  - プロパティ経由でデータを受け取る
  - イベントはコールバックで親に通知

### ui/controllers/
- **役割**: UIイベントとビジネスロジックの橋渡し。
- **責務**:
  - ユーザー操作の受付
  - services/ 層の呼び出し
  - UI の更新指示

### ui/styles/
- **役割**: UIのビジュアルスタイル定義。
- **責務**:
  - 色、フォント、余白などの定数管理
  - スタイルの一元管理で変更を容易に

### utils/
- **役割**: 汎用的なヘルパー機能。
- **責務**:
  - ファイルI/O、日時処理、テキスト処理など
  - 他の層から横断的に利用される

## 3. データフロー

```
User Action
    ↓
[UI Components] ← イベント受付
    ↓
[Controllers] ← イベントハンドリング
    ↓
[Services] ← ビジネスロジック実行
    ↓
[Models] ← データ更新
    ↓
[Data Service] ← JSON保存
    ↓
[Controllers] → UI更新指示
    ↓
[UI Components] ← 再レンダリング
```

## 4. 主要なクラス/モジュール

### models/prompt.py
```python
@dataclass
class Prompt:
    id: str
    title: str
    body: str
    category_path: List[str]
    favorite: bool
    deleted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
```

### models/category.py
```python
@dataclass
class Category:
    id: str
    name: str
    parent_id: Optional[str]
    order: int
```

### models/app_state.py
```python
class AppState:
    prompts: List[Prompt]
    categories: List[Category]
    trash: List[str]  # prompt IDs
    selected_category: Optional[str]
    search_query: str
    current_editing: Optional[str]  # prompt ID
```

### services/data_service.py
- `load_data() -> AppState`
- `save_data(state: AppState) -> None`
- `create_backup() -> None`

### services/prompt_service.py
- `create_prompt(title, body, category_path) -> Prompt`
- `update_prompt(id, **kwargs) -> Prompt`
- `delete_prompt(id) -> None`
- `restore_prompt(id) -> None`
- `get_filtered_prompts(category, search, favorite) -> List[Prompt]`

### ui/controllers/main_controller.py
- `on_add_prompt()`
- `on_card_click(prompt_id)`
- `on_delete_prompt(prompt_id)`
- `on_copy_prompt(prompt_id)`
- `on_toggle_favorite(prompt_id)`
- `on_category_change(category_id)`
- `on_search(query)`

## 5. 状態管理の方針

- **単一のグローバル状態**: `AppState` を `main.py` で保持
- **イミュータブル更新**: 状態は常に新しいオブジェクトで置き換え
- **自動保存**: 状態変更後、デバウンス付きで JSON 保存
- **リアクティブUI**: 状態変更時に関連する UI コンポーネントを再描画

## 6. エラーハンドリング

- **JSON読み込み失敗**: バックアップから復元 or 空データで起動
- **JSON書き込み失敗**: ロールバック＋エラーメッセージ
- **カテゴリ階層エラー**: 操作キャンセル＋理由説明
- **すべてのエラー**: `utils/logger.py` でログ記録

## 7. 実装の優先順位

### Phase 1: 基盤（必須）
1. models/ - データモデル定義
2. services/data_service.py - JSON読み書き
3. services/prompt_service.py - 基本CRUD
4. ui/styles/ - スタイル定義

### Phase 2: コアUI（必須）
5. ui/components/card/prompt_card.py - カード表示
6. ui/views/card_grid_view.py - グリッド表示
7. ui/components/editor/ - 編集UI
8. ui/views/edit_view.py - 編集ビュー
9. ui/controllers/main_controller.py - メインコントローラー

### Phase 3: カテゴリ（重要）
10. services/category_service.py - カテゴリ管理
11. ui/components/sidebar/category_tree.py - カテゴリツリー
12. ui/components/sidebar/category_item.py - ドラッグ&ドロップ

### Phase 4: 追加機能（重要）
13. services/undo_service.py - アンドゥ管理
14. ui/views/trash_view.py - ゴミ箱
15. services/clipboard_service.py - コピー機能
16. ui/components/common/snackbar.py - 通知

### Phase 5: 検索・その他（低優先）
17. services/search_service.py - 検索機能
18. ui/components/sidebar/search_box.py - 検索UI
19. ui/controllers/keyboard_controller.py - キーボード操作

## 8. コーディング規約

- **命名**: PEP 8準拠（snake_case、CamelCase）
- **型ヒント**: すべての関数に型アノテーション
- **Docstring**: Google Style
- **インポート**: 標準ライブラリ → サードパーティ → ローカル
- **1ファイル1クラス原則**: コンポーネントは1ファイルに1つ

## 9. 依存関係

```
main.py
  └─ ui/app.py
      ├─ ui/views/
      │   └─ ui/components/
      │       └─ ui/controllers/
      │           └─ services/
      │               └─ models/
      └─ ui/styles/

utils/ は全層から参照可能
```

## 10. テストの方針

- **services/**: ユニットテスト必須（ビジネスロジック）
- **models/**: データクラスのバリデーションテスト
- **ui/components/**: 可能な範囲で統合テスト
- **utils/**: ユニットテスト必須（汎用関数）
