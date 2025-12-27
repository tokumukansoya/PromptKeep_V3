# PromptKeep - AI実行マスターガイド

このドキュメントは、Roo Code（GitHub Copilot）がPromptKeepを**完全に自律的に実装**するための実行ガイドです。

---

## � ドキュメント駆動開発の原則

### ⭐️ 金科玉条: ドキュメントファースト

```
新機能追加・仕様変更の場合：

1️⃣ ドキュメントを先に更新 📝
   ↓
2️⃣ Gitコミット（docs: ...）
   ↓
3️⃣ コードを実装 🔧
   ↓
4️⃣ Gitコミット（feat/fix: ...）
```

**理由**:
- ドキュメントが実装の指針になる
- AIが最新の仕様を参照できる
- ドキュメントとコードの不一致を防ぐ

### 更新対象ドキュメント

| ケース | 更新するドキュメント |
|------|------------------|
| 新機能追加 | requirements.md, architecture.md, implementation_plan.md, ai_execution_guide.md |
| 仕様変更 | 該当箇所 + 関連ドキュメント |
| バグ修正 | 不要（仕様通りなら） |

---

## �📌 このドキュメントの使い方

### 開発者向け
1. 実装したいPhaseのセクションを開く
2. 「🤖 AI実行コマンド」をコピー
3. Roo Codeに貼り付けて実行
4. 「✅ 成功確認チェックリスト」で検証

### AI（Roo Code）向け
- このドキュメントの各Phaseセクションは**完全な実行指示書**です
- 「AI実行コマンド」を受け取ったら、以下を順次実行してください：
  1. 必要なファイルを作成
  2. コーディング規約に従って実装
  3. 検証可能なコードを生成
  4. 成功確認チェックリストに基づいて自己検証

---

## 🎯 前提条件（必須確認）

```yaml
環境:
  Python: 3.14.2
  Flet: 0.28.3
  パッケージ管理: uv
  OS: Linux

ディレクトリ構造:
  存在確認: PromptKeep_V3/ 以下が正しく配置されているか
  
必須ドキュメント:
  - docs/requirements.md      # 機能要件
  - docs/architecture.md      # アーキテクチャ設計
  - docs/coding_style.md      # コーディング規約
  - docs/implementation_plan.md  # 実装計画
  - docs/ai_prompts.md        # AIプロンプトテンプレート集
```

---

## 📊 Phase実装マップ

```
Phase 0: 基盤セットアップ（✅ 完了想定）
  ↓
Phase 1: データモデル層（✅ 完了想定）
  ↓
Phase 2: ビジネスロジック層
  ├─→ Phase 2-1: CategoryService
  ├─→ Phase 2-2: UndoService
  ├─→ Phase 2-3: ClipboardService
  └─→ Phase 2-4: SearchService
  ↓
Phase 3: UIスタイル定義（✅ 完了想定）
  ↓
Phase 4: UIコアコンポーネント
  ├─→ Phase 4-1: CardBody
  ├─→ Phase 4-2: CardHeader
  ├─→ Phase 4-3: PromptCard
  ├─→ Phase 4-4: CardGridView
  └─→ Phase 4-5: Snackbar
  ↓
Phase 5: 編集機能
  ├─→ Phase 5-1: TitleField, BodyField
  ├─→ Phase 5-2: CategorySelector
  ├─→ Phase 5-3: EditorToolbar
  ├─→ Phase 5-4: EditView統合
  └─→ Phase 5-5: EditController + 自動保存
  ↓
Phase 6: サイドバー・カテゴリ管理
  ├─→ Phase 6-1: SearchBox
  ├─→ Phase 6-2: AddCategoryDialog
  ├─→ Phase 6-3: CategoryItem（D&D対応）
  ├─→ Phase 6-4: CategoryTree
  ├─→ Phase 6-5: Sidebar統合
  └─→ Phase 6-6: CategoryController
  ↓
Phase 7: メイン画面統合
  ├─→ Phase 7-1: MainView
  ├─→ Phase 7-2: App.py
  └─→ Phase 7-3: MainController + main.py
  ↓
Phase 8: ゴミ箱機能
  ├─→ Phase 8-1: TrashView
  └─→ Phase 8-2: TrashController
  ↓
Phase 9: キーボード操作
  └─→ Phase 9-1: KeyboardController
  ↓
Phase 10: 検索・フィルタ（低優先）
  └─→ Phase 10-1: Search統合
  ↓
Phase 11: エラーハンドリング
  └─→ Phase 11-1: エラーハンドリング強化
  ↓
Phase 12: テスト・最適化
  └─→ Phase 12-1: 統合テスト
```

---

## 🚀 Phase 2: ビジネスロジック層

### Phase 2-1: CategoryService 実装

#### 🤖 AI実行コマンド

```markdown
【PromptKeep Phase 2-1: CategoryService 実装】

## Git操作（Phase開始時）
```bash
git checkout main
git pull origin main
git checkout -b phase-2-1-category-service
```

## タスク概要
カテゴリのCRUD操作と階層管理を実装してください。

## 環境
- Python: 3.14.2
- Flet: 0.28.3
- パッケージ管理: uv

## 対象ファイル
- `services/category_service.py`（新規作成）

## 実装要件

### 1. CategoryServiceクラスの作成

```python
class CategoryService:
    """カテゴリのCRUD操作と階層管理を提供するサービス。
    
    Attributes:
        data_service: データ永続化サービス
        logger: ロガーインスタンス
    """
    
    def __init__(self, data_service: DataService):
        """初期化
        
        Args:
            data_service: DataServiceのインスタンス
        """
        pass
```

### 2. 実装メソッド一覧

#### create_category
```python
def create_category(
    self,
    state: AppState,
    name: str,
    parent_id: Optional[str] = None
) -> Category:
    """新しいカテゴリを作成する。
    
    Args:
        state: アプリケーション状態
        name: カテゴリ名
        parent_id: 親カテゴリのID（Noneの場合はルートレベル）
    
    Returns:
        作成されたCategoryオブジェクト
    
    Raises:
        InvalidCategoryDepthError: 階層が最大深度を超える場合
        CategoryNotFoundError: 親カテゴリが存在しない場合
    """
```

#### update_category
```python
def update_category(
    self,
    state: AppState,
    category_id: str,
    name: str
) -> Category:
    """カテゴリ名を更新する。
    
    Args:
        state: アプリケーション状態
        category_id: 更新対象のカテゴリID
        name: 新しいカテゴリ名
    
    Returns:
        更新されたCategoryオブジェクト
    
    Raises:
        CategoryNotFoundError: カテゴリが存在しない場合
    """
```

#### delete_category
```python
def delete_category(
    self,
    state: AppState,
    category_id: str
) -> None:
    """カテゴリを削除する（論理削除）。
    
    子カテゴリも再帰的に削除し、紐づくプロンプトは未分類に移動する。
    
    Args:
        state: アプリケーション状態
        category_id: 削除対象のカテゴリID
    
    Raises:
        CategoryNotFoundError: カテゴリが存在しない場合
    """
```

#### get_category
```python
def get_category(
    self,
    state: AppState,
    category_id: str
) -> Optional[Category]:
    """IDでカテゴリを取得する。
    
    Args:
        state: アプリケーション状態
        category_id: 取得対象のカテゴリID
    
    Returns:
        見つかったCategoryオブジェクト、存在しない場合はNone
    """
```

#### list_categories
```python
def list_categories(
    self,
    state: AppState,
    parent_id: Optional[str] = None
) -> List[Category]:
    """カテゴリ一覧を取得する。
    
    Args:
        state: アプリケーション状態
        parent_id: 親カテゴリID（Noneの場合は全カテゴリ）
    
    Returns:
        カテゴリのリスト（orderでソート済み）
    """
```

#### move_category
```python
def move_category(
    self,
    state: AppState,
    category_id: str,
    new_parent_id: Optional[str]
) -> Category:
    """カテゴリを別の親の下に移動する（ドラッグ&ドロップ対応）。
    
    Args:
        state: アプリケーション状態
        category_id: 移動対象のカテゴリID
        new_parent_id: 新しい親カテゴリのID（Noneの場合はルートへ）
    
    Returns:
        移動後のCategoryオブジェクト
    
    Raises:
        InvalidCategoryDepthError: 移動後の階層が最大深度を超える場合
        CategoryNotFoundError: カテゴリが存在しない場合
        ValueError: 自分自身または子孫カテゴリへの移動を試みた場合
    
    Note:
        UI層ではドロップ前にcan_move_to()で検証し、視覚フィードバックを提供すること。
    """
```

#### can_move_to
```python
def can_move_to(
    self,
    state: AppState,
    category_id: str,
    target_parent_id: Optional[str]
) -> bool:
    """カテゴリが指定された親カテゴリに移動可能かを判定する。
    
    Args:
        state: アプリケーション状態
        category_id: 移動対象のカテゴリID
        target_parent_id: 移動先の親カテゴリID
    
    Returns:
        移動可能な場合True、不可の場合False
    
    Note:
        - 自分自身への移動: False
        - 子孫カテゴリへの移動: False
        - 最大階層超過: False
        - UI層でドラッグ中の視覚フィードバックに使用
    """
```

#### validate_depth
```python
def validate_depth(
    self,
    state: AppState,
    category_id: str,
    target_parent_id: Optional[str]
) -> bool:
    """カテゴリ移動時の階層深度を検証する。
    
    Args:
        state: アプリケーション状態
        category_id: 検証対象のカテゴリID
        target_parent_id: 移動先の親カテゴリID
    
    Returns:
        階層深度が有効な場合True、超過する場合False
    """
```

#### get_category_path
```python
def get_category_path(
    self,
    state: AppState,
    category_id: str
) -> List[str]:
    """カテゴリIDからルートまでのパス（名前のリスト）を取得する。
    
    Args:
        state: アプリケーション状態
        category_id: 対象のカテゴリID
    
    Returns:
        ルートからのカテゴリ名のリスト（例: ["親", "子", "孫"]）
    """
```

### 3. 階層制約
- 最大階層深度: `config.MAX_CATEGORY_DEPTH`（3階層）
- 階層超過時は`InvalidCategoryDepthError`を発生
- 循環参照の防止

### 4. エラーハンドリング
- すべての例外は`exceptions.py`で定義済みのものを使用
- `logger.error()`でエラーログを出力
- トランザクション的な動作（エラー時はロールバック）

### 5. 依存関係
- `models.category.Category`
- `models.app_state.AppState`
- `services.data_service.DataService`
- `config.MAX_CATEGORY_DEPTH`
- `exceptions.CategoryNotFoundError, InvalidCategoryDepthError`
- `utils.logger`

## コーディング規約
- [docs/coding_style.md](coding_style.md)に完全準拠
- 型ヒント必須（すべての引数・戻り値）
- Google Style Docstring必須
- インポート順序: 標準ライブラリ → サードパーティ → ローカル

## 参考ドキュメント
- アーキテクチャ: [docs/architecture.md](architecture.md)
- 要件定義: [docs/requirements.md](requirements.md)
- 実装計画: [docs/implementation_plan.md](implementation_plan.md)
- 参考実装: services/prompt_service.py

## 実装完了条件
✅ すべてのメソッドが実装されている
✅ 型ヒントとDocstringが完備
✅ 階層制約の検証が正しく動作
✅ エラーハンドリングが適切
✅ logging出力が適切

## Git操作（実装完了時）
```bash
# ファイルをステージング
git add services/category_service.py

# コミット
git commit -m "feat: Phase 2-1 CategoryService 実装完了"

# 必要に応じてmainにマージ（Phase完了時）
git checkout main
git merge phase-2-1-category-service
git push origin main
git branch -d phase-2-1-category-service
```
```

#### ✅ 成功確認チェックリスト

```markdown
## Phase 2-1 成功確認

### ファイル作成確認
- [ ] `services/category_service.py`が作成されている

### コード品質確認
- [ ] すべてのメソッドに型ヒントがある
- [ ] すべてのメソッドにGoogle Style Docstringがある
- [ ] インポート順序が正しい（標準→サードパーティ→ローカル）
- [ ] config.MAX_CATEGORY_DEPTHを使用している

### 機能確認（手動テスト用）
- [ ] create_category()が動作する
- [ ] 最大3階層まで作成できる
- [ ] 4階層目を作成しようとするとInvalidCategoryDepthErrorが発生する
- [ ] update_category()でカテゴリ名を変更できる
- [ ] delete_category()でカテゴリを削除できる
- [ ] move_category()でカテゴリを移動できる
- [ ] 移動時の階層制約が正しく検証される

### エラーハンドリング確認
- [ ] 存在しないカテゴリIDでCategoryNotFoundErrorが発生する
- [ ] すべてのエラーでlogger.error()が呼ばれている

### 依存関係確認
- [ ] DataServiceをインポートしている
- [ ] AppState, Categoryをインポートしている
- [ ] exceptions.pyの例外をインポートしている
```

---

### Phase 2-2: UndoService 実装

#### 🤖 AI実行コマンド

```markdown
【PromptKeep Phase 2-2: UndoService 実装】

## タスク概要
削除操作のアンドゥ機能を実装してください。直前の1操作のみ保持します。

## 環境
- Python: 3.14.2
- Flet: 0.28.3

## 対象ファイル
- `services/undo_service.py`（新規作成）

## 実装要件

### 1. UndoServiceクラスの作成

```python
class UndoService:
    """アンドゥ・リドゥ機能を提供するサービス。
    
    直前の削除操作を1ステップのみ保持する。
    
    Attributes:
        max_stack_size: スタックの最大サイズ（デフォルト: 1）
        undo_stack: アンドゥスタック
        logger: ロガーインスタンス
    """
    
    def __init__(self, max_stack_size: int = 1):
        """初期化
        
        Args:
            max_stack_size: スタックの最大サイズ
        """
        pass
```

### 2. 実装メソッド一覧

#### push_state
```python
def push_state(self, operation: str, data: Dict[str, Any]) -> None:
    """現在の状態をスタックにプッシュする。
    
    Args:
        operation: 操作の種類（"delete_prompt", "delete_category"など）
        data: 復元に必要なデータ（Promptオブジェクトのdict表現など）
    """
```

#### can_undo
```python
def can_undo(self) -> bool:
    """アンドゥ可能かどうかを返す。
    
    Returns:
        スタックが空でない場合True
    """
```

#### undo
```python
def undo(self) -> Optional[Dict[str, Any]]:
    """直前の操作をアンドゥする。
    
    Returns:
        アンドゥ情報の辞書、スタックが空の場合None
        辞書のキー: "operation", "data"
    """
```

#### clear
```python
def clear(self) -> None:
    """スタックをクリアする。"""
```

### 3. データ構造
```python
# スタックに保存する構造
{
    "operation": "delete_prompt",
    "data": {
        "id": "uuid",
        "title": "string",
        "body": "string",
        # ... その他のPromptフィールド
    }
}
```

### 4. 制約
- スタックサイズは1（直前の操作のみ保持）
- 新しい操作をプッシュすると古い操作は削除される

### 5. 依存関係
- `typing.Dict, Any, Optional`
- `utils.logger`

## コーディング規約
- [docs/coding_style.md](coding_style.md)に完全準拠
- 型ヒント必須
- Google Style Docstring必須

## 参考ドキュメント
- 要件定義: [docs/requirements.md](requirements.md)（アンドゥ機能の説明）
- アーキテクチャ: [docs/architecture.md](architecture.md)

## 実装完了条件
✅ すべてのメソッドが実装されている
✅ 型ヒントとDocstringが完備
✅ スタックサイズ制限が正しく動作
✅ logging出力が適切
```

#### ✅ 成功確認チェックリスト

```markdown
## Phase 2-2 成功確認

### ファイル作成確認
- [ ] `services/undo_service.py`が作成されている

### コード品質確認
- [ ] すべてのメソッドに型ヒントがある
- [ ] すべてのメソッドにGoogle Style Docstringがある
- [ ] インポート順序が正しい

### 機能確認（手動テスト用）
- [ ] push_state()で状態を保存できる
- [ ] can_undo()が正しくTrue/Falseを返す
- [ ] undo()でスタックから状態を取得できる
- [ ] スタックサイズが1に制限されている（2つ目をプッシュすると1つ目が消える）
- [ ] clear()でスタックをクリアできる

### ログ確認
- [ ] undo()実行時にlogger.info()が呼ばれる
```

---

### Phase 2-3: ClipboardService 実装

#### 🤖 AI実行コマンド

```markdown
【PromptKeep Phase 2-3: ClipboardService 実装】

## タスク概要
Fletのクリップボード機能を使って、プロンプト本文をコピーする機能を実装してください。

## 環境
- Python: 3.14.2
- Flet: 0.28.3

## 対象ファイル
- `services/clipboard_service.py`（新規作成）

## 実装要件

### 1. ClipboardServiceクラスの作成

```python
class ClipboardService:
    """クリップボード操作を提供するサービス。
    
    Attributes:
        logger: ロガーインスタンス
    """
    
    def __init__(self):
        """初期化"""
        pass
```

### 2. 実装メソッド一覧

#### copy_to_clipboard
```python
def copy_to_clipboard(self, page: ft.Page, text: str) -> bool:
    """テキストをクリップボードにコピーする。
    
    Args:
        page: Fletのページオブジェクト
        text: コピーするテキスト
    
    Returns:
        成功した場合True、失敗した場合False
    """
```

#### get_clipboard_text
```python
def get_clipboard_text(self, page: ft.Page) -> Optional[str]:
    """クリップボードからテキストを取得する。
    
    Args:
        page: Fletのページオブジェクト
    
    Returns:
        クリップボードのテキスト、取得失敗時はNone
    """
```

### 3. Flet Clipboard API使用方法
```python
# コピー
page.set_clipboard(text)

# 取得
clipboard_text = page.get_clipboard()
```

### 4. エラーハンドリング
- try-exceptでラップ
- 失敗時は`logger.error()`でログ出力
- 失敗時はFalseまたはNoneを返す

### 5. 依存関係
- `flet as ft`
- `typing.Optional`
- `utils.logger`

## コーディング規約
- [docs/coding_style.md](coding_style.md)に完全準拠
- 型ヒント必須
- Google Style Docstring必須

## 参考ドキュメント
- Flet Clipboard API: https://flet.dev/docs/controls/page#clipboard
- 要件定義: [docs/requirements.md](requirements.md)

## 実装完了条件
✅ copy_to_clipboard()が実装されている
✅ get_clipboard_text()が実装されている
✅ 型ヒントとDocstringが完備
✅ エラーハンドリングが適切
```

#### ✅ 成功確認チェックリスト

```markdown
## Phase 2-3 成功確認

### ファイル作成確認
- [ ] `services/clipboard_service.py`が作成されている

### コード品質確認
- [ ] すべてのメソッドに型ヒントがある
- [ ] すべてのメソッドにGoogle Style Docstringがある
- [ ] Flet 0.28.3のAPIを使用している

### 機能確認（手動テスト用）
- [ ] copy_to_clipboard()でテキストをコピーできる
- [ ] get_clipboard_text()でクリップボードから取得できる
- [ ] エラー時にFalse/Noneが返る

### エラーハンドリング確認
- [ ] try-exceptでラップされている
- [ ] logger.error()が適切に呼ばれる
```

---

### Phase 2-4: SearchService 実装

#### 🤖 AI実行コマンド

```markdown
【PromptKeep Phase 2-4: SearchService 実装】

## タスク概要
プロンプトの検索・フィルタリング機能を実装してください。

## 環境
- Python: 3.14.2
- Flet: 0.28.3

## 対象ファイル
- `services/search_service.py`（新規作成）

## 実装要件

### 1. SearchServiceクラスの作成

```python
class SearchService:
    """検索・フィルタリング機能を提供するサービス。
    
    Attributes:
        logger: ロガーインスタンス
    """
    
    def __init__(self):
        """初期化"""
        pass
```

### 2. 実装メソッド一覧

#### search_prompts
```python
def search_prompts(
    self,
    prompts: List[Prompt],
    query: str
) -> List[Prompt]:
    """タイトルと本文で検索する。
    
    大文字小文字を区別せず、部分一致で検索する。
    
    Args:
        prompts: 検索対象のプロンプトリスト
        query: 検索クエリ
    
    Returns:
        マッチしたプロンプトのリスト
    """
```

#### filter_by_category
```python
def filter_by_category(
    self,
    prompts: List[Prompt],
    category_ids: List[str]
) -> List[Prompt]:
    """カテゴリでフィルタする。
    
    Args:
        prompts: フィルタ対象のプロンプトリスト
        category_ids: カテゴリIDリスト（例: ["cat1_id", "cat2_id"]）
    
    Returns:
        マッチしたプロンプトのリスト
    """
```

#### filter_by_favorite
```python
def filter_by_favorite(
    self,
    prompts: List[Prompt]
) -> List[Prompt]:
    """お気に入りでフィルタする。
    
    Args:
        prompts: フィルタ対象のプロンプトリスト
    
    Returns:
        お気に入りのプロンプトリスト
    """
```

#### apply_filters
```python
def apply_filters(
    self,
    prompts: List[Prompt],
    query: Optional[str] = None,
    category_ids: Optional[List[str]] = None,
    favorite_only: bool = False
) -> List[Prompt]:
    """複数のフィルタを組み合わせて適用する。
    
    Args:
        prompts: フィルタ対象のプロンプトリスト
        query: 検索クエリ（Noneの場合は検索しない）
        category_ids: カテゴリIDリスト（Noneの場合はフィルタしない）
        favorite_only: お気に入りのみ表示するか
    
    Returns:
        フィルタ後のプロンプトリスト
    """
```

### 3. 検索ロジック
- タイトル（`title`）と本文（`body`）の両方を対象
- `str.lower()`で小文字変換して比較
- `in`演算子で部分一致検索

### 4. カテゴリフィルタロジック
- `category_ids`が完全一致するものを抽出
- 空リスト`[]`は「未分類」として扱う

### 5. 依存関係
- `models.prompt.Prompt`
- `typing.List, Optional`
- `utils.logger`

## コーディング規約
- [docs/coding_style.md](coding_style.md)に完全準拠
- 型ヒント必須
- Google Style Docstring必須

## 参考ドキュメント
- 要件定義: [docs/requirements.md](requirements.md)（検索機能の説明）
- アーキテクチャ: [docs/architecture.md](architecture.md)

## 実装完了条件
✅ すべてのメソッドが実装されている
✅ 検索が大文字小文字を区別しない
✅ 複数フィルタの組み合わせが動作する
✅ 型ヒントとDocstringが完備
```

#### ✅ 成功確認チェックリスト

```markdown
## Phase 2-4 成功確認

### ファイル作成確認
- [ ] `services/search_service.py`が作成されている

### コード品質確認
- [ ] すべてのメソッドに型ヒントがある
- [ ] すべてのメソッドにGoogle Style Docstringがある
- [ ] インポート順序が正しい

### 機能確認（手動テスト用）
- [ ] search_prompts()でタイトル検索ができる
- [ ] search_prompts()で本文検索ができる
- [ ] 大文字小文字を区別しない（"test"で"Test"がヒット）
- [ ] filter_by_category()でカテゴリフィルタができる
- [ ] filter_by_favorite()でお気に入りフィルタができる
- [ ] apply_filters()で複数条件を組み合わせられる

### ログ確認
- [ ] 検索実行時にlogger.info()が呼ばれる（任意）
```

---

## 🚀 Phase 4: UIコアコンポーネント

### Phase 4-1: CardBody 実装

#### 🤖 AI実行コマンド

```markdown
【PromptKeep Phase 4-1: CardBody 実装】

## タスク概要
カードの本文部分（タイトル + プレビュー）を実装してください。

## 環境
- Python: 3.14.2
- Flet: 0.28.3

## 対象ファイル
- `ui/components/card/card_body.py`（新規作成）

## 実装要件

### 1. CardBodyクラスの作成

```python
class CardBody(ft.Container):
    """プロンプトカードの本文部分（タイトル + プレビュー）。
    
    Attributes:
        prompt: 表示対象のPromptオブジェクト
    """
    
    def __init__(self, prompt: Prompt):
        """初期化
        
        Args:
            prompt: 表示するPromptオブジェクト
        """
        super().__init__()
        self.prompt = prompt
        self._build()
```

### 2. レイアウト構造

```
Container (カード本文部分)
├── Column
    ├── Text (タイトル)
    │   ├── weight: bold
    │   ├── size: FONT_SIZE_MEDIUM
    │   ├── max_lines: 2
    │   └── overflow: ellipsis
    └── Text (本文プレビュー)
        ├── size: FONT_SIZE_SMALL
        ├── max_lines: 3
        ├── overflow: ellipsis
        └── color: TEXT_SECONDARY
```

### 3. プレビュー生成
```python
from utils.text_utils import create_preview

# 40〜80文字のプレビューを生成
preview_text = create_preview(self.prompt.body, max_length=80)
```

### 4. スタイル定義
```python
from ui.styles.colors import TEXT_PRIMARY, TEXT_SECONDARY
from ui.styles.typography import FONT_SIZE_SMALL, FONT_SIZE_MEDIUM
from ui.styles.spacing import PADDING_SMALL

# タイトル
ft.Text(
    value=self.prompt.title,
    color=TEXT_PRIMARY,
    size=FONT_SIZE_MEDIUM,
    weight=ft.FontWeight.BOLD,
    max_lines=2,
    overflow=ft.TextOverflow.ELLIPSIS
)

# プレビュー
ft.Text(
    value=preview_text,
    color=TEXT_SECONDARY,
    size=FONT_SIZE_SMALL,
    max_lines=3,
    overflow=ft.TextOverflow.ELLIPSIS
)
```

### 5. 依存関係
- `flet as ft`
- `models.prompt.Prompt`
- `ui.styles.colors`
- `ui.styles.typography`
- `ui.styles.spacing`
- `utils.text_utils.create_preview`

## コーディング規約
- [docs/coding_style.md](coding_style.md)に完全準拠
- 型ヒント必須
- Google Style Docstring必須
- Flet 0.28.3のコンポーネントを使用

## 参考ドキュメント
- アーキテクチャ: [docs/architecture.md](architecture.md)（UIコンポーネント構造）
- 要件定義: [docs/requirements.md](requirements.md)（カード表示の仕様）
- スタイル定義: ui/styles/*.py

## 実装完了条件
✅ CardBodyクラスが実装されている
✅ タイトルとプレビューが正しく表示される
✅ プレビューが40〜80文字に制限されている
✅ スタイルが適用されている
✅ 型ヒントとDocstringが完備
```

#### ✅ 成功確認チェックリスト

```markdown
## Phase 4-1 成功確認

### ファイル作成確認
- [ ] `ui/components/card/card_body.py`が作成されている

### コード品質確認
- [ ] クラスがft.Containerを継承している
- [ ] 型ヒントが完備されている
- [ ] Google Style Docstringが記載されている
- [ ] スタイル定数をインポートしている

### 機能確認（後のPhaseで視覚的に確認）
- [ ] タイトルが太字で表示される
- [ ] プレビューが3行まで表示される
- [ ] 長いテキストは省略記号（...）で切れる
- [ ] テキスト色が適切（タイトル: TEXT_PRIMARY、プレビュー: TEXT_SECONDARY）

### デザイン確認
- [ ] フォントサイズが適切
- [ ] 行間・余白が適切
```

---

### Phase 4-2: CardHeader 実装

#### 🤖 AI実行コマンド

```markdown
【PromptKeep Phase 4-2: CardHeader 実装】

## タスク概要
カードのヘッダー部分（お気に入り★ + コピーボタン）を実装してください。

## 環境
- Python: 3.14.2
- Flet: 0.28.3

## 対象ファイル
- `ui/components/card/card_header.py`（新規作成）

## 実装要件

### 1. CardHeaderクラスの作成

```python
class CardHeader(ft.Container):
    """プロンプトカードのヘッダー（お気に入り + コピーボタン）。
    
    Attributes:
        prompt: 表示対象のPromptオブジェクト
        on_favorite_toggle: お気に入りトグル時のコールバック
        on_copy: コピーボタンクリック時のコールバック
    """
    
    def __init__(
        self,
        prompt: Prompt,
        on_favorite_toggle: Optional[Callable[[str], None]] = None,
        on_copy: Optional[Callable[[str], None]] = None
    ):
        """初期化
        
        Args:
            prompt: 表示するPromptオブジェクト
            on_favorite_toggle: お気に入りトグル時のコールバック（引数: prompt_id）
            on_copy: コピーボタンクリック時のコールバック（引数: prompt_id）
        """
        super().__init__()
        self.prompt = prompt
        self.on_favorite_toggle = on_favorite_toggle
        self.on_copy = on_copy
        self._build()
```

### 2. レイアウト構造

```
Container (ヘッダー部分)
└── Row (alignment=space_between)
    ├── IconButton (お気に入り★)
    │   ├── icon: star (お気に入りの場合) / star_border (それ以外)
    │   ├── icon_color: ACCENT_COLOR (お気に入りの場合) / TEXT_SECONDARY (それ以外)
    │   └── on_click: _handle_favorite_toggle
    └── IconButton (コピー)
        ├── icon: content_copy
        ├── icon_color: TEXT_SECONDARY
        └── on_click: _handle_copy
```

### 3. イベントハンドラ

```python
def _handle_favorite_toggle(self, e):
    """お気に入りトグル処理。"""
    if self.on_favorite_toggle:
        self.on_favorite_toggle(self.prompt.id)

def _handle_copy(self, e):
    """コピーボタンクリック処理。"""
    if self.on_copy:
        self.on_copy(self.prompt.id)
```

### 4. アイコン選択ロジック

```python
# お気に入りアイコン
favorite_icon = ft.icons.STAR if self.prompt.favorite else ft.icons.STAR_BORDER
favorite_color = ACCENT_COLOR if self.prompt.favorite else TEXT_SECONDARY
```

### 5. スタイル定義

```python
from ui.styles.colors import ACCENT_COLOR, TEXT_SECONDARY
from ui.styles.spacing import PADDING_SMALL

ft.IconButton(
    icon=favorite_icon,
    icon_color=favorite_color,
    icon_size=20,
    on_click=self._handle_favorite_toggle
)

ft.IconButton(
    icon=ft.icons.CONTENT_COPY,
    icon_color=TEXT_SECONDARY,
    icon_size=18,
    on_click=self._handle_copy
)
```

### 6. 依存関係
- `flet as ft`
- `typing.Callable, Optional`
- `models.prompt.Prompt`
- `ui.styles.colors`
- `ui.styles.spacing`

## コーディング規約
- [docs/coding_style.md](coding_style.md)に完全準拠
- 型ヒント必須（Callable型を含む）
- Google Style Docstring必須

## 参考ドキュメント
- アーキテクチャ: [docs/architecture.md](architecture.md)
- 要件定義: [docs/requirements.md](requirements.md)（お気に入りとコピー機能）
- Flet Icons: https://flet.dev/docs/controls/icon

## 実装完了条件
✅ CardHeaderクラスが実装されている
✅ お気に入りトグルボタンが動作する
✅ コピーボタンが動作する
✅ アイコンの色が適切に変わる
✅ 型ヒントとDocstringが完備
```

#### ✅ 成功確認チェックリスト

```markdown
## Phase 4-2 成功確認

### ファイル作成確認
- [ ] `ui/components/card/card_header.py`が作成されている

### コード品質確認
- [ ] クラスがft.Containerを継承している
- [ ] Callable型ヒントが使用されている
- [ ] Google Style Docstringが記載されている

### 機能確認（後のPhaseで視覚的に確認）
- [ ] お気に入りボタンが表示される
- [ ] お気に入り状態でアイコンが変わる（star / star_border）
- [ ] お気に入り状態で色が変わる（ACCENT_COLOR / TEXT_SECONDARY）
- [ ] コピーボタンが表示される
- [ ] ボタンクリックでコールバックが呼ばれる

### デザイン確認
- [ ] アイコンサイズが適切
- [ ] 配置が右寄せ（space_between）
```

---

### Phase 4-3: PromptCard 実装

#### 🤖 AI実行コマンド

```markdown
【PromptKeep Phase 4-3: PromptCard 実装】

## タスク概要
CardHeaderとCardBodyを統合し、完全なプロンプトカードを実装してください。

## 環境
- Python: 3.14.2
- Flet: 0.28.3

## 対象ファイル
- `ui/components/card/prompt_card.py`（新規作成）

## 実装要件

### 1. PromptCardクラスの作成

```python
class PromptCard(ft.Container):
    """プロンプトカード全体（ヘッダー + ボディ）。
    
    正方形のカードとして表示される。
    
    Attributes:
        prompt: 表示対象のPromptオブジェクト
        on_click: カードクリック時のコールバック
        on_favorite_toggle: お気に入りトグル時のコールバック
        on_copy: コピーボタンクリック時のコールバック
    """
    
    def __init__(
        self,
        prompt: Prompt,
        on_click: Optional[Callable[[str], None]] = None,
        on_favorite_toggle: Optional[Callable[[str], None]] = None,
        on_copy: Optional[Callable[[str], None]] = None
    ):
        """初期化
        
        Args:
            prompt: 表示するPromptオブジェクト
            on_click: カードクリック時のコールバック（引数: prompt_id）
            on_favorite_toggle: お気に入りトグル時のコールバック
            on_copy: コピーボタンクリック時のコールバック
        """
        super().__init__()
        self.prompt = prompt
        self.on_click = on_click
        self.on_favorite_toggle = on_favorite_toggle
        self.on_copy = on_copy
        self._build()
```

### 2. レイアウト構造

```
Container (カード全体 - 正方形)
├── width: CARD_WIDTH
├── height: CARD_HEIGHT (= CARD_WIDTH、正方形)
├── bgcolor: CARD_BG
├── border_radius: BORDER_RADIUS
├── padding: PADDING_MEDIUM
├── on_click: _handle_click
└── Column
    ├── CardHeader (お気に入り + コピーボタン)
    ├── Divider (optional)
    └── CardBody (タイトル + プレビュー)
```

### 3. カードスタイル

```python
from ui.styles.card_style import CARD_WIDTH, CARD_HEIGHT, CARD_BG, BORDER_RADIUS
from ui.styles.spacing import PADDING_MEDIUM
from ui.styles.colors import HOVER_COLOR

self.content = ft.Column(
    controls=[
        CardHeader(
            prompt=self.prompt,
            on_favorite_toggle=self.on_favorite_toggle,
            on_copy=self.on_copy
        ),
        ft.Divider(height=1, color=TEXT_SECONDARY, opacity=0.3),
        CardBody(prompt=self.prompt)
    ],
    spacing=8
)

self.width = CARD_WIDTH
self.height = CARD_HEIGHT
self.bgcolor = CARD_BG
self.border_radius = BORDER_RADIUS
self.padding = PADDING_MEDIUM
self.on_click = self._handle_click

# ホバーエフェクト（任意）
self.animate = ft.animation.Animation(100, ft.AnimationCurve.EASE_IN_OUT)
```

### 4. イベントハンドラ

```python
def _handle_click(self, e):
    """カードクリック処理。"""
    if self.on_click:
        self.on_click(self.prompt.id)
```

### 5. 依存関係
- `flet as ft`
- `typing.Callable, Optional`
- `models.prompt.Prompt`
- `ui.components.card.card_header.CardHeader`
- `ui.components.card.card_body.CardBody`
- `ui.styles.card_style`
- `ui.styles.colors`
- `ui.styles.spacing`

## コーディング規約
- [docs/coding_style.md](coding_style.md)に完全準拠
- 型ヒント必須
- Google Style Docstring必須

## 参考ドキュメント
- アーキテクチャ: [docs/architecture.md](architecture.md)
- 要件定義: [docs/requirements.md](requirements.md)（カード形状: 正方形）
- スタイル定義: ui/styles/card_style.py

## 実装完了条件
✅ PromptCardクラスが実装されている
✅ CardHeaderとCardBodyが統合されている
✅ カードが正方形（width == height）である
✅ カードクリックでコールバックが呼ばれる
✅ 型ヒントとDocstringが完備
```

#### ✅ 成功確認チェックリスト

```markdown
## Phase 4-3 成功確認

### ファイル作成確認
- [ ] `ui/components/card/prompt_card.py`が作成されている

### コード品質確認
- [ ] クラスがft.Containerを継承している
- [ ] CardHeaderとCardBodyを使用している
- [ ] 型ヒントが完備されている
- [ ] Google Style Docstringが記載されている

### 機能確認（後のPhaseで視覚的に確認）
- [ ] カードが正方形で表示される
- [ ] ヘッダー（お気に入り + コピー）が表示される
- [ ] ボディ（タイトル + プレビュー）が表示される
- [ ] カードクリックでコールバックが呼ばれる
- [ ] 背景色・角丸が適用されている

### デザイン確認
- [ ] CARD_WIDTH == CARD_HEIGHT
- [ ] パディングが適切
- [ ] ホバーエフェクトがある（任意）
```

---

## 📚 補足情報

### ドキュメント参照優先順位

AI実行時は以下の順で参照してください：

1. **本ファイル（ai_execution_guide.md）** - 実行指示の詳細
2. **coding_style.md** - コーディング規約
3. **requirements.md** - 機能要件
4. **architecture.md** - アーキテクチャ設計
5. **implementation_plan.md** - 実装計画の全体像
6. **ai_prompts.md** - 補助的なテンプレート

### エラー発生時の対応

AI実行中にエラーが発生した場合：

1. **エラーメッセージを確認**
2. **coding_style.md の該当箇所を再確認**
3. **依存関係の実装状況を確認**（Phase依存）
4. **Flet 0.28.3のAPIドキュメントを確認**

### 次Phaseへの移行条件

各Phaseの「成功確認チェックリスト」がすべて✅になったら、次のPhaseに進んでください。

---

## 🔄 更新履歴

- 2025-12-27: 初版作成（Phase 2, Phase 4の一部）
- 今後、Phase 5以降も順次追加予定

---

**注意**: このドキュメントは継続的に更新されます。実装前に最新版を確認してください。
