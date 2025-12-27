# PromptKeep 要件定義（Flet）

> **AI実装ガイド**: このドキュメントは実装時の判断基準として使用してください。不明点は [ai_execution_guide.md](ai_execution_guide.md) を参照してください。

---

## 🎯 クイックサマリー（AI向け最重要情報）

```yaml
技術スタック:
  言語: Python 3.14.2
  フレームワーク: Flet 0.28.3
  パッケージ管理: uv
  データ永続化: JSON (ローカル)
  
アプリ概要:
  種類: デスクトップアプリ（クロスプラットフォーム）
  テーマ: ダークテーマ固定
  UI構造: 左サイドバー + 右カードグリッド/編集ビュー
  
核心機能:
  - プロンプトのCRUD操作（作成・読取・更新・削除）
  - カテゴリ階層管理（最大3階層）
  - お気に入り機能
  - ワンクリックコピー
  - ゴミ箱（無期限保持）
  - アンドゥ（Ctrl+Z）
  
制約条件:
  - カテゴリ階層: 最大3階層まで
  - 本文プレビュー: 40〜80文字
  - カード形状: 正方形
  - 自動保存: デバウンス2〜3秒
  - オフライン動作: 完全ローカル
```

---

## 1. 目的
- プロンプトをローカルで安全に管理・閲覧・編集・コピーするシンプルなデスクトップアプリを提供する。
- 階層カテゴリとお気に入りで整理し、カード表示で素早く参照できることを重視。

## 2. スコープ
- Flet を用いたデスクトップアプリ（ダークテーマ固定）。
- ローカル JSON ファイルへの永続化。クラウド連携やインポート/エクスポートは対象外。
- シングルユーザー前提。マルチユーザーや認証は対象外。

## 3. 想定ユーザー / ユースケース
- プロンプトを日常的に作成・整理する個人ユーザー。
- よく使うプロンプトをカードで素早くコピーし、必要に応じて編集する。
- カテゴリ階層（最大 3 階層）で整理し、お気に入りで横断的に参照する。

## 4. データモデル（ローカル JSON）

### 4.1 ファイルパス
- `data/prompts.json` に保存（存在しない場合は自動生成）
- バックアップ: `data/backup/prompts_YYYYMMDD_HHMMSS.json`

### 4.2 JSONスキーマ（AI実装時の正確な型定義）

```json
{
  "prompts": [
    {
      "id": "string (UUID v4)",
      "title": "string (必須)",
      "body": "string (必須)",
      "category_ids": ["cat_id_1", "cat_id_2", "cat_id_3"],
      "favorite": "boolean (デフォルト: false)",
      "deleted_at": "string (ISO8601) | null",
      "created_at": "string (ISO8601, 必須)",
      "updated_at": "string (ISO8601, 必須)"
    }
  ],
  "categories": [
    {
      "id": "string (UUID v4)",
      "name": "string (必須)",
      "parent_id": "string (UUID v4) | null",
      "order": "number (整数, デフォルト: 0)"
    }
  ],
  "trash": {
    "prompts": ["prompt_id1", "prompt_id2"],
    "categories": ["category_id1"]
  }
}
```

### 4.3 データ制約（必須検証）

| フィールド | 制約 | 検証タイミング |
|-----------|------|--------------|
| `category_ids` | 最大3要素（3階層まで）、**IDベース** | カテゴリ移動・作成時 |
| `category_ids` | 空配列 `[]` = 未分類 | 常時 |
| `id` | UUID v4形式 | 作成時 |
| `deleted_at` | null = 通常, ISO8601 = 削除済み | 削除時 |
| `parent_id` | null = ルートレベル | カテゴリ作成時 |

**重要**: `category_ids`はカテゴリ名ではなく**カテゴリID**の配列。カテゴリ名変更時もプロンプトは影響を受けない。

## 5. 機能要件（優先度順・AI実装時の判断基準）

### 5.1 【Must】プロンプトCRUD操作（最優先）

#### 作成（Create）
```yaml
トリガー: 「+新規」ボタンクリック
動作:
  1. 空のPromptオブジェクトを生成（id: UUID, title: "", body: ""）
  2. 編集ビューを開く
  3. 自動保存が有効化される
検証: タイトル・本文を入力後、JSON に保存される
```

#### 読取（Read）
```yaml
トリガー: アプリ起動時、カテゴリ選択時、検索時
動作:
  1. data/prompts.json を読み込み
  2. deleted_at が null のもののみ表示
  3. カードグリッドに表示
検証: JSON のデータがカードとして表示される
```

#### 更新（Update）
```yaml
トリガー: 編集ビューでテキスト入力
動作:
  1. 入力後 2〜3 秒デバウンス
  2. updated_at を現在時刻に更新
  3. JSON に自動保存
保存失敗時: エラーログ + ユーザーに通知
検証: 編集内容が自動的に JSON に反映される
```

#### 削除（Delete）
```yaml
トリガー: カード上の削除ボタン
動作:
  1. deleted_at に現在時刻を設定（論理削除）
  2. ゴミ箱に移動
  3. スナックバーで通知「削除しました」
  4. アンドゥスタックに状態を保存
確認ダイアログ: なし（即時削除）
検証: カード一覧から消え、ゴミ箱に表示される
```

---

### 5.2 【Must】カード表示（Core UI）

#### カードレイアウト（正方形・固定仕様）
```yaml
形状: 正方形（width == height）
サイズ: CARD_WIDTH = 200px, CARD_HEIGHT = 200px
配置: GridView でレスポンシブに列数調整
背景色: CARD_BG（ダークテーマ）
角丸: BORDER_RADIUS = 8px
```

#### カード構成要素
```
┌─────────────────────┐
│ ★  📋（コピー）     │ ← CardHeader
├─────────────────────┤
│ タイトル（太字）     │ ← CardBody
│ 本文プレビュー...   │   （40〜80文字）
│ （2〜3行表示）      │
└─────────────────────┘
```

#### コピー機能（ワンクリック）
```yaml
トリガー: カード右上のコピーアイコンクリック
動作:
  1. プロンプト本文（body）をクリップボードにコピー
  2. スナックバーで通知「コピーしました」
API: page.set_clipboard(text)
検証: クリップボードに本文が保存される
```

#### お気に入り機能
```yaml
トリガー: カード左上の★クリック
動作:
  1. favorite フィールドをトグル（true ⇔ false）
  2. アイコン変更（STAR ⇔ STAR_BORDER）
  3. アイコン色変更（ACCENT_COLOR ⇔ TEXT_SECONDARY）
  4. JSON に自動保存
検証: ★の状態が永続化される
```

---

### 5.3 【Must】カテゴリ階層管理（最大3階層）

#### カテゴリ作成
```yaml
トリガー: サイドバー下部の「+ カテゴリ追加」ボタン
動作:
  1. ダイアログ表示（名前入力 + 親カテゴリ選択）
  2. 階層深度を検証（最大3階層）
  3. Categoryオブジェクト作成
  4. JSON に保存
エラー: 4階層目を作成しようとすると InvalidCategoryDepthError
検証: 3階層まで作成でき、4階層目は拒否される
```

#### ドラッグ&ドロップ（ListTile + Draggable/DragTarget）
```yaml
実装方式: ListTile + ft.Draggable/DragTarget
階層表現: インデントで階層を視覚化（├ └ 記号使用）

動作:
  1. カテゴリアイテムをドラッグ開始（Draggable）
  2. ドロップ先のカテゴリにホバー時、強調表示（DragTarget）
  3. ドロップ時、移動後の階層深度を検証
  4. 検証OKなら parent_id を更新し JSON に保存
  5. 検証NGなら元の位置に戻す

制約:
  - 自分自身へのドロップ: 不可（変更なし）
  - 子孫カテゴリへのドロップ: 不可（循環参照防止）
  - 最大階層超過: 不可（スナックバーで通知）

視覚フィードバック:
  - ドラッグ中: 半透明表示
  - ドロップ可能: 緑のボーダー
  - ドロップ不可: 赤のボーダー

検証: D&D で階層を変更でき、制約が守られる
```

---

### 5.4 【Must】編集ビュー（自動保存）

#### レイアウト
```
┌─────────────────────────────┐
│ [← 戻る]                     │ ← EditorToolbar
├─────────────────────────────┤
│ タイトル: [_____________]    │ ← TitleField
├─────────────────────────────┤
│ カテゴリ: [選択ドロップダウン] │ ← CategorySelector
├─────────────────────────────┤
│ 本文:                        │ ← BodyField
│ [                           │
│  テキストエリア（複数行）     │
│                             │
│ ]                           │
└─────────────────────────────┘
```

#### 自動保存ロジック（StateManagerで実装）
```python
# StateManagerによるデバウンス実装（AI実装時の参考）
class StateManager:
    def __init__(self, page, data_service, debounce_seconds=2.0):
        self._page = page
        self._save_task = None
        self._debounce_seconds = debounce_seconds
    
    def update_prompts(self, prompts):
        \"\"\"プロンプトリストを更新し、自動保存をスケジュール。\"\"\"
        self._state.prompts = prompts
        self._notify_listeners()  # UI更新
        self._schedule_save()  # デバウンス付き保存
    
    def _schedule_save(self):
        if self._save_task:
            self._save_task.cancel()
        # Flet推奨: page.run_task()を使用
        self._save_task = self._page.run_task(self._debounced_save)
    
    async def _debounced_save(self):
        await asyncio.sleep(self._debounce_seconds)
        self._data_service.save_data(self._state)

# EditControllerはStateManagerを呼ぶだけ
class EditController:
    def on_text_change(self, new_text):
        prompt = self._update_prompt_text(new_text)
        prompts = self._replace_prompt(prompt)
        self.state_manager.update_prompts(prompts)  # これだけでOK
```

---

### 5.5 【Must】ゴミ箱機能

#### ゴミ箱表示
```yaml
トリガー: サイドバーの「ゴミ箱」アイテムクリック
表示内容: deleted_at が null でないプロンプト一覧
操作:
  - 復元ボタン: deleted_at を null に戻す
  - 完全削除: JSON から完全に削除
  - ゴミ箱を空にする: 全削除
保持期間: 無期限
検証: 削除したプロンプトがゴミ箱に表示される
```

---

### 5.6 【Must】アンドゥ機能（Ctrl+Z）

```yaml
対象操作: 削除のみ（1ステップ）
トリガー: Ctrl+Z キー
動作:
  1. UndoService.undo() を呼び出し
  2. スタックから直前の状態を取得
  3. Prompt を復元（deleted_at を null に）
  4. スナックバーで通知「復元しました」
制約: 直前の1操作のみ保持
検証: 削除直後に Ctrl+Z で復元できる
```

---

### 5.7 【Should】検索・フィルタ（低優先）

#### 検索機能
```yaml
対象: タイトル（title）+ 本文（body）
方式: 部分一致、大文字小文字を区別しない
実装: SearchService.search_prompts(prompts, query)
検証: "test" で "Testing" を検索できる
```

#### フィルタ機能
```yaml
カテゴリフィルタ: category_ids で絞り込み
お気に入りフィルタ: favorite == true のみ表示
組み合わせ: AND 条件で複数フィルタ適用
検証: カテゴリ選択 + お気に入りで絞り込める
```

---

### 5.8 【Must】UI/UX

#### ダークテーマ（固定）
```yaml
背景色: DARK_BG = "#1E1E1E"
カード背景: CARD_BG = "#2D2D2D"
テキスト: TEXT_PRIMARY = "#FFFFFF", TEXT_SECONDARY = "#B0B0B0"
アクセント: ACCENT_COLOR = "#BB86FC"
```

#### フィードバック（スナックバー）
```yaml
表示位置: 右下
表示時間: 2〜3秒（duration=2000〜3000ミリ秒）
メッセージ例:
  - "コピーしました"
  - "削除しました"
  - "復元しました"
  - "保存しました"
スタイル: 控えめ（小さめ、半透明）
実装: ft.SnackBar + page.open()
```

#### レスポンシブレイアウト
```yaml
ウィンドウサイズ変更対応:
  - page.on_resized イベントで検知
  - GridViewの列数を動的調整
  - 計算式: runs_count = max(1, int(page.width / 220))
    # カード幅200px + 余白20px
初期サイズ:
  - WINDOW_WIDTH = 1200px
  - WINDOW_HEIGHT = 800px
最小サイズ: 800x600px（推奨）
```

## 6. 非機能要件（実装時の技術的制約）

### 6.1 パフォーマンス要件
```yaml
起動時間: 3秒以内（1,000件のプロンプトでも）
スクロール: 60fps を維持
検索応答: 100ms以内（デバウンス後）
自動保存: 2〜3秒のデバウンス
対応件数: 1,000〜10,000件のプロンプトでも快適に動作

パフォーマンス対策:
  - カードグリッド: ページネーション（50件/ページ）または仮想スクロール
  - 検索インデックス: カテゴリ・お気に入りのインデックス構造
  - 遅延ロード: 初期表示は最小限、スクロールで追加読み込み
  
実装方針:
  - 1,000件超えの場合はページネーションを採用
  - カテゴリ・お気に入りはインデックスで高速フィルタリング
```

### 6.2 データ永続化・信頼性
```yaml
書き込み方式: アトミック（テンポラリファイル経由）
エラーハンドリング:
  - 読み込み失敗: バックアップから復旧 → 空データで起動
  - 書き込み失敗: ロールバック + エラー通知
バックアップ:
  - 自動バックアップ: 起動時・保存前
  - パス: data/backup/prompts_YYYYMMDD_HHMMSS.json
  - 保持期間: 最新10件（任意）
```

### 6.3 アクセシビリティ
```yaml
キーボード操作:
  - Tab: フォーカス移動
  - Enter: 決定
  - Escape: キャンセル・戻る
  - Ctrl+Z: アンドゥ
  - Ctrl+C: コピー（コンテキスト依存）
  - Ctrl+F: 検索フォーカス（任意）
色コントラスト:
  - WCAG AA基準以上
  - テキストと背景のコントラスト比 4.5:1 以上
```

### 6.4 オフライン動作
```yaml
ネットワーク: 不要（完全ローカル）
外部依存: なし（Flet内蔵機能のみ）
クラウド連携: 対象外
```

---

## 7. 画面/コンポーネント要件（AI実装時の構造図）

### 7.1 メイン画面レイアウト

```
┌─────────────────────────────────────────────────┐
│                 PromptKeep                      │ ← AppBar（任意）
├──────────┬──────────────────────────────────────┤
│          │                                      │
│ サイドバー │  カードグリッド / 編集ビュー          │
│          │                                      │
│ [検索]   │  ┌────┐ ┌────┐ ┌────┐              │
│          │  │Card│ │Card│ │Card│              │
│ カテゴリ   │  └────┘ └────┘ └────┘              │
│ ├ 仕事    │  ┌────┐ ┌────┐ ┌────┐              │
│ ├ 趣味    │  │Card│ │Card│ │Card│              │
│ └ その他  │  └────┘ └────┘ └────┘              │
│          │                                      │
│ お気に入り │  または                              │
│ ゴミ箱    │                                      │
│          │  ┌──────────────────────┐            │
│ [+ カテゴリ]│  │  編集ビュー          │            │
│          │  │  タイトル: [____]    │            │
│          │  │  本文: [________]    │            │
│          │  └──────────────────────┘            │
└──────────┴──────────────────────────────────────┘
```

### 7.2 左サイドバー（Sidebar）

```python
# 構成コンポーネント
Sidebar
├── SearchBox              # 検索ボックス
├── Divider
├── CategoryTree           # カテゴリツリー（ListTile+ドラッグ対応）
│   ├── Draggable(CategoryItem) (ルート1)
│   │   ├── Draggable(CategoryItem) (├ 子1-1)  # インデント表示
│   │   └── Draggable(CategoryItem) (└ 子1-2)  # インデント表示
│   └── Draggable(CategoryItem) (ルート2)
├── Divider
├── ListTile (お気に入り)
├── ListTile (ゴミ箱)
└── AddCategoryButton      # カテゴリ追加ボタン

# 階層表現：インデント + 記号
# Level 0: カテゴリ名
# Level 1: ├ カテゴリ名
# Level 2:   └ カテゴリ名
```

### 7.3 右ペイン（カードグリッド / 編集ビュー切り替え）

#### カードグリッドビュー
```python
CardGridView
├── AppBar (任意)
│   └── IconButton (+ 新規プロンプト)
└── GridView (レスポンシブ)
    ├── PromptCard
    ├── PromptCard
    └── ... (100〜1000件対応)
```

#### 編集ビュー
```python
EditView
├── EditorToolbar
│   ├── IconButton (← 戻る)
│   └── Text (自動保存中...)
├── TitleField              # タイトル入力
├── CategorySelector        # カテゴリ選択
└── BodyField               # 本文テキストエリア
```

---

## 8. 状態管理 / 振る舞い（AI実装時のロジック詳細）

### 8.1 状態管理方式

```python
# AppState（models/app_state.py）
@dataclass
class AppState:
    """アプリケーション全体の状態。"""
    prompts: List[Prompt]
    categories: List[Category]
    trash_prompt_ids: List[str]
    trash_category_ids: List[str]
    
    # UI状態
    selected_category_id: Optional[str] = None
    search_query: str = ""
    show_favorites_only: bool = False
    current_view: str = "grid"  # "grid" | "edit" | "trash"
    editing_prompt_id: Optional[str] = None
```

### 8.2 ビュー切り替えロジック

```python
# MainController の例
class MainController:
    def show_card_grid(self):
        """カードグリッドビューを表示。"""
        self.state.current_view = "grid"
        self.state.editing_prompt_id = None
        self.page.update()
    
    def show_edit_view(self, prompt_id: str):
        """編集ビューを表示。"""
        self.state.current_view = "edit"
        self.state.editing_prompt_id = prompt_id
        self.page.update()
    
    def show_trash_view(self):
        """ゴミ箱ビューを表示。"""
        self.state.current_view = "trash"
        self.page.update()
```

### 8.3 アンドゥスタック管理

```python
# UndoService の使用例
undo_service = UndoService(max_stack_size=1)

# 削除時
def delete_prompt(prompt_id: str):
    prompt = prompt_service.get_prompt(state, prompt_id)
    # スタックに現在の状態を保存
    undo_service.push_state("delete_prompt", prompt.to_dict())
    # 削除実行
    prompt_service.delete_prompt(state, prompt_id)

# アンドゥ時
def handle_undo():
    if undo_service.can_undo():
        undo_data = undo_service.undo()
        if undo_data["operation"] == "delete_prompt":
            prompt_service.restore_prompt(state, undo_data["data"]["id"])
```

### 8.4 ドラッグ&ドロップ処理（ListTile + Draggable/DragTarget）

```python
# CategoryItem のドラッグ処理例
def on_drag_will_accept(e: ft.DragTargetEvent):
    """ドロップ可否を判定し、視覚フィードバックを提供。"""
    dragged_id = e.src_id
    target_id = e.control.data
    
    # 自分自身・子孫・階層超過のチェック
    can_accept = category_service.can_move_to(
        state,
        category_id=dragged_id,
        target_parent_id=target_id
    )
    
    # ボーダー色変更でフィードバック
    e.control.content.border = ft.border.all(
        2, ft.Colors.GREEN if can_accept else ft.Colors.RED
    )
    e.control.update()

def on_drag_accept(e: ft.DragTargetAcceptEvent):
    """カテゴリのドロップを受け入れる。"""
    dragged_id = e.src_id  # ドラッグされたカテゴリID
    target_id = e.control.data  # ドロップ先のカテゴリID
    
    try:
        # 階層検証付きで移動
        category_service.move_category(
            state,
            category_id=dragged_id,
            new_parent_id=target_id
        )
        # 成功通知
        show_snackbar("カテゴリを移動しました")
    except InvalidCategoryDepthError as e:
        show_snackbar(e.user_message)
    except ValueError as e:
        show_snackbar(str(e))

def on_drag_leave(e: ft.DragTargetEvent):
    """ドラッグが離れた時、ボーダーをリセット。"""
    e.control.content.border = None
    e.control.update()
```

---

## 9. エラーハンドリング（AI実装時の例外処理）

### 9.1 カスタム例外（exceptions.py で定義済み）

```python
# 使用する例外一覧
class PromptNotFoundError(Exception):
    """プロンプトが見つからない場合。"""

class CategoryNotFoundError(Exception):
    """カテゴリが見つからない場合。"""

class InvalidCategoryDepthError(Exception):
    """カテゴリ階層が最大深度を超える場合。"""

class DataLoadError(Exception):
    """JSONデータの読み込みに失敗した場合。"""

class DataSaveError(Exception):
    """JSONデータの保存に失敗した場合。"""
```

### 9.2 エラーハンドリングパターン

```python
# Pattern 1: サービス層でのエラーハンドリング
def create_category(state, name, parent_id):
    try:
        # 階層検証
        if not validate_depth(state, None, parent_id):
            raise InvalidCategoryDepthError("最大3階層まで")
        
        # カテゴリ作成
        category = Category(...)
        state.categories.append(category)
        
        # 保存
        data_service.save(state)
        logger.info(f"カテゴリ作成成功: {name}")
        return category
        
    except InvalidCategoryDepthError as e:
        logger.error(f"カテゴリ作成失敗: {e}")
        raise  # UI層で処理
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        raise

# Pattern 2: UI層でのエラーハンドリング
def handle_create_category(name, parent_id):
    try:
        category = category_service.create_category(
            state, name, parent_id
        )
        show_snackbar("カテゴリを作成しました")
        
    except InvalidCategoryDepthError:
        show_snackbar("最大3階層までです", error=True)
        
    except Exception as e:
        show_snackbar(f"エラーが発生しました: {e}", error=True)
```

### 9.3 JSON読み書きエラー処理

```python
# DataService での例
def load_data(self) -> AppState:
    """JSONファイルからデータを読み込む。"""
    try:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return self._parse_state(data)
        
    except FileNotFoundError:
        logger.warning("JSONファイルが存在しません。空データで初期化します。")
        return self._create_empty_state()
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析エラー: {e}")
        # バックアップから復旧を試みる
        return self._load_from_backup()
        
    except Exception as e:
        logger.error(f"データ読み込みエラー: {e}")
        raise DataLoadError(f"データの読み込みに失敗しました: {e}")
```

---

## 10. 優先度（AI実装時の判断基準）

### 10.1 優先度マトリックス

| 優先度 | 機能 | 理由 |
|-------|-----|-----|
| **Must（必須）** | プロンプトCRUD | コア機能 |
| **Must** | カード表示 | メインUI |
| **Must** | カテゴリ管理（3階層） | 整理機能 |
| **Must** | お気に入り | 頻繁に使う機能 |
| **Must** | コピー機能 | 最も使う操作 |
| **Must** | ゴミ箱 | 安全性 |
| **Must** | アンドゥ（Ctrl+Z） | UX向上 |
| **Must** | 自動保存 | データ保護 |
| **Should（重要）** | カテゴリD&D | UX向上 |
| **Should** | 検索・フィルタ | 効率化 |
| **Could（任意）** | 仮想スクロール | パフォーマンス最適化 |
| **Could** | カードアニメーション | UX向上 |
| **Won't（対象外）** | クラウド連携 | スコープ外 |
| **Won't** | インポート/エクスポート | スコープ外 |

---

## 11. 開発メモ（AI実装時の参考情報）

### 11.1 Flet コンポーネント選択ガイド

```python
# UI要素とFletコンポーネントの対応
カード表示 → ft.Container + ft.Column
カードグリッド → ft.GridView (child_aspect_ratio=1.0 で正方形)
サイドバー → ft.NavigationRail または ft.Container
カテゴリツリー → ft.Column + ft.ListTile + ft.Draggable/DragTarget
  ├ 階層表現: ListTile の leading_width でインデント
  ├ ドラッグ: ft.Draggable でラップ
  └ ドロップ: ft.DragTarget でラップ
テキスト入力 → ft.TextField (multiline=False)
本文入力 → ft.TextField (multiline=True, min_lines=10)
カテゴリ選択 → ft.Dropdown
ボタン → ft.ElevatedButton, ft.IconButton
通知 → ft.SnackBar (右下、2〜3秒表示)
ダイアログ → ft.AlertDialog
```

### 11.2 ファイルパス定数（config.py）

```python
# AI実装時に使用する定数
DATA_DIR = "data"
JSON_FILE = "data/prompts.json"
BACKUP_DIR = "data/backup"
MAX_CATEGORY_DEPTH = 3
PREVIEW_LENGTH_MIN = 40
PREVIEW_LENGTH_MAX = 80
AUTO_SAVE_DEBOUNCE = 2.5  # 秒
```

### 11.3 ID 生成

```python
import uuid

# プロンプトID
prompt_id = str(uuid.uuid4())

# カテゴリID
category_id = str(uuid.uuid4())
```

---

## 12. 確定済み仕様（変更不可）

以下の仕様は確定しており、AI実装時に変更しないでください：

```yaml
本文プレビュー文字数: 40〜80文字（可変、省略記号付き）
カード形状: 正方形（width == height）
カードサイズ: 200x200px（CARD_WIDTH, CARD_HEIGHT）
検索対象: タイトル + 本文全体
カテゴリ階層: 最大3階層（厳守）
編集ビュー: 自動保存（確認ダイアログなし）
削除: 即時実行（確認ダイアログなし）
ゴミ箱: 無期限保持
アンドゥ: 直前1操作のみ
テーマ: ダークテーマ固定
データ形式: JSON（ローカル）
```

---

## 13. AI実装時のチェックリスト

各機能実装後、以下を確認してください：

```markdown
### 機能実装確認
- [ ] 要件定義に記載された動作を満たしている
- [ ] データ制約（階層、文字数など）が守られている
- [ ] エラーハンドリングが適切に実装されている
- [ ] ログ出力が適切に行われている

### コード品質確認
- [ ] 型ヒントが完備されている
- [ ] Docstringが記載されている（Google Style）
- [ ] coding_style.md に準拠している
- [ ] 定数を config.py から読み込んでいる

### UI/UX確認
- [ ] ダークテーマが適用されている
- [ ] スナックバーで適切なフィードバックがある
- [ ] レスポンシブに動作する（画面幅変更時）
- [ ] キーボード操作に対応している

### データ永続化確認
- [ ] JSON に正しく保存される
- [ ] アプリ再起動後もデータが保持される
- [ ] バックアップが作成される
```

---

**参考ドキュメント**:
- 実装ガイド: [ai_execution_guide.md](ai_execution_guide.md) ← **AI実装時はこちらを優先**
- アーキテクチャ: [architecture.md](architecture.md)
- コーディング規約: [coding_style.md](coding_style.md)
- 実装計画: [implementation_plan.md](implementation_plan.md)
