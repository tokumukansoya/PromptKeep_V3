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
│   ├── prompt.py                    # Promptモデル（id, title, body, category_ids, favorite, etc.）
│   ├── category.py                  # Categoryモデル（id, name）  # フラットカテゴリ（parent_id 未使用）
│   └── app_state.py                 # アプリ全体の状態管理
│
├── services/                        # ビジネスロジック層
│   ├── __init__.py
│   ├── state_manager.py             # **状態管理の中核**（新設）
│   ├── data_service.py              # データ永続化サービス（JSON読み書き）
│   ├── prompt_service.py            # プロンプトCRUD操作
│   ├── category_service.py          # カテゴリCRUD操作（シンプル・フラット）
│   ├── search_service.py            # 検索・フィルタリングロジック
│   └── clipboard_service.py         # クリップボード操作
  # アンドゥはゴミ箱復元で代替（独立した UndoService の実装は必須ではありません）
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
│   │   │   └── category_list.py     # カテゴリ一覧（フラット）
│   │   │
│   │   ├── card/                    # カード関連（簡素化）
│   │   │   ├── __init__.py
│   │   │   └── prompt_card.py       # プロンプトカード全体
│   │   │
│   │   ├── editor/                  # 編集エリア関連
│   │   │   ├── __init__.py
│   │   │   ├── title_field.py       # タイトル入力フィールド
│   │   │   ├── body_field.py        # 本文テキストエリア
│   │   │   └── category_selector.py # カテゴリ選択UI
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
  - AppState（アプリ全体の状態コンテナ）
  - データの型定義とバリデーション
- **重要**: category_ids は**IDベース**でカテゴリ名変更の影響を受けない

### services/
- **役割**: ビジネスロジックの実装。UIから独立して動作。
- **責務**:
  - **StateManager**: 状態管理の中核。全ての状態変更を統括、デバウンス付き自動保存
  - **PromptService/CategoryService**: ビジネスロジックのみ。状態変更はStateManagerに委譲
  - **DataService**: JSON読み書きの低レベル操作
  - 検索・フィルタリング
  - クリップボード操作
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
    category_ids: List[str]  # IDベース（名前ではない）
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
@dataclass
class AppState:
    prompts: List[Prompt]
    categories: List[Category]
    trash_prompt_ids: List[str]
    trash_category_ids: List[str]
    selected_category_id: Optional[str]
    search_query: str
    current_editing_id: Optional[str]
```

### services/state_manager.py（新設・重要）
```python
class StateManager:
    \"\"\"状態管理の中核。全ての状態変更はここを経由する。\"\"\"
    
    def __init__(self, page: ft.Page, data_service: DataService):
        self._page = page
        self._state = AppState.empty()
        self._data_service = data_service
        self._listeners = []
    
    # 状態変更メソッド
    def update_prompts(self, prompts: List[Prompt]):
        self._state.prompts = prompts
        self._notify_listeners()
        self._schedule_save()  # デバウンス付き自動保存
    
    def _schedule_save(self):
        if self._save_task:
            self._save_task.cancel()
        # Flet推奨: page.run_task()でバックグラウンドタスク実行
        self._save_task = self._page.run_task(self._debounced_save)
    
    # リスナー管理
    def add_listener(self, callback):
        self._listeners.append(callback)
```

### services/data_service.py
- `load_data() -> AppState`
- `save_data(state: AppState) -> None`
- `create_backup() -> None`

### services/prompt_service.py
```python
class PromptService:
    \"\"\"ビジネスロジックのみ。状態変更はStateManagerに委譲。\"\"\"
    
    def create_prompt(self, title: str, body: str, category_ids: List[str]) -> Prompt:
        # Promptオブジェクトを生成して返すだけ
        return Prompt.create(title, body, category_ids)
    
    def validate_category_depth(self, category_ids: List[str]) -> bool:
        # フラットカテゴリのため階層制約は不要（常に True）
        return True  # noqa: D401
```

### ui/controllers/main_controller.py
```python
class MainController:
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        self.state_manager.add_listener(self._on_state_changed)
    
    def on_add_prompt(self):
        prompt = self.prompt_service.create_prompt(...)
        prompts = self.state_manager.state.prompts + [prompt]
        self.state_manager.update_prompts(prompts)  # StateManagerを経由
```

## 5. 状態管理の方針（重要な設計決定）

### StateManager方式を採用
- **単一責任**: StateManagerが状態管理・永続化・通知を統括
- **デバウンス自動保存**: 2秒のデバウンス付きで自動保存
- **Controller分離**: 各ControllerはStateManagerを経由して状態変更
- **リアクティブUI**: リスナーパターンでUI更新を通知

### データフロー
```
User Action
    ↓
[Controller] ← イベント受付
    ↓
[Service] ← ビジネスロジック（Promptオブジェクト生成など）
    ↓
[StateManager] ← 状態更新 + デバウンス付き保存
    ↓
[Listeners] → UI自動更新
```

### 重要な制約
- **Controllerは状態を直接変更しない**: 必ずStateManagerのメソッドを呼ぶ
- **Serviceは状態を持たない**: 純粋な関数として実装
- **category_idsはIDベース**: カテゴリ名変更時もプロンプトは影響を受けない

## 6. エラーハンドリング

### 例外の統一的な処理
```python
class BaseController:
    def handle_error(self, error: Exception):
        if isinstance(error, PromptKeeperError):
            self.show_snackbar(error.user_message)  # ユーザーフレンドリーなメッセージ
            logger.warning(str(error))
        else:
            self.show_snackbar("予期しないエラーが発生しました")
            logger.error(f"Unexpected error: {error}", exc_info=True)
```

### エラー種別
- **JSON読み込み失敗**: バックアップから復元 or 空データで起動
- **JSON書き込み失敗**: DataPersistenceErrorをスロー、ユーザーに通知
- **カテゴリ階層エラー**: InvalidCategoryDepthError（ユーザーメッセージ付き）
- **すべてのエラー**: `utils/logger.py` で自動ログ記録

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
10. services/category_service.py - カテゴリ管理（フラット）
11. ui/components/sidebar/category_list.py - カテゴリ一覧（ListTile）
12. ui/components/sidebar/category_item.py - ListTile

### Phase 4: 追加機能（重要）
13. (Undo service removed - use trash restore)
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
