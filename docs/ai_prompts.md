# AI 指示用テンプレート集

> **重要**: このドキュメントは補助的なテンプレート集です。**実装時は [ai_execution_guide.md](ai_execution_guide.md) を優先的に参照してください。**

このドキュメントは、各 Phase を実装する際に GitHub Copilot や Roo Code にコピペで使えるテンプレート集です。

---

## 📋 使い方

### 推奨フロー（Roo Code向け）
1. **まず [ai_execution_guide.md](ai_execution_guide.md) を確認**
   - 詳細な実行コマンドと成功確認チェックリストがあります
   - Phase間の依存関係と全体マップも記載されています

2. **このドキュメントの使い方**
   - ai_execution_guide.md に記載のないPhaseのテンプレートを参照
   - 既存のテンプレートをカスタマイズする際の参考として使用

### 基本的な使い方
1. 実装したい Phase のテンプレートをコピー
2. `[TODO]` 部分を必要に応じて編集（通常はそのままでOK）
3. GitHub Copilot / Roo Code に貼り付け
4. 生成されたコードを確認
5. [docs/coding_style.md](coding_style.md) のチェックリストで検証

---

## 📚 ドキュメント参照優先順位

AI実装時は以下の順で参照してください：

1. ⭐️ **[ai_execution_guide.md](ai_execution_guide.md)** - 最優先・最も詳細
2. **[coding_style.md](coding_style.md)** - コーディング規約
3. **[requirements.md](requirements.md)** - 機能要件（最適化済み）
4. **[architecture.md](architecture.md)** - アーキテクチャ設計
5. **[implementation_plan.md](implementation_plan.md)** - 実装計画の全体像
6. 📄 **本ファイル（ai_prompts.md）** - 補助的なテンプレート

---

## Phase 0: 環境セットアップ（✅ 完了）

このフェーズは完了済みです。

---

## Phase 1: データモデル層（✅ 完了）

このフェーズは完了済みです。

---

## Phase 2: ビジネスロジック層

> **注意**: Phase 2の詳細な実行コマンドは [ai_execution_guide.md](ai_execution_guide.md) を参照してください。
> 
> 以下は補助的なテンプレートです。

### Phase 2-1: CategoryService 実装

```markdown
【Phase 2-1: CategoryService 実装】

詳細は [ai_execution_guide.md](ai_execution_guide.md) の Phase 2-1 セクションを参照してください。

以下は簡易版テンプレートです：

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- services/category_service.py

要件：
カテゴリの CRUD 操作を実装してください。

実装内容：
1. CategoryService クラスの作成
   - __init__(self, data_service: DataService)
   - create_category(state, name, parent_id=None) -> Category
   - update_category(state, category_id, name) -> Category
   - delete_category(state, category_id) -> None
   - get_category(state, category_id) -> Category
   - list_categories(state) -> List[Category]
   - move_category(state, category_id, new_parent_id) -> Category
   - validate_depth(category_ids: List[str]) -> bool

2. カテゴリ階層の検証
   - 最大 3 階層まで（config.MAX_CATEGORY_DEPTH）
   - 循環参照の防止
   - 親カテゴリの存在確認

3. エラーハンドリング
   - CategoryNotFoundError
   - InvalidCategoryDepthError
   - logger.error() でログ出力

依存：
- Phase 1（models/category.py, models/app_state.py）完了
- services/data_service.py 完了

規約厳守事項：
- 型ヒント：すべての関数に Optional/Union/List などを明記
- Docstring：Google Style で記載
- 定数：config.py から MAX_CATEGORY_DEPTH をインポート
- エラー：logger.error() でコンソール出力
- コメント：Docstring と明白でない処理のみ

参考ドキュメント：
- アーキテクチャ: docs/architecture.md
- 要件定義: docs/requirements.md
- コーディング規約: docs/coding_style.md
- 実装計画: docs/implementation_plan.md
- 参考実装: services/prompt_service.py
```

### Phase 2-2: UndoService 実装

```markdown
【Phase 2-2: UndoService 実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- services/undo_service.py

要件：
アンドゥ機能を実装してください。直前の削除操作を1ステップ戻せるようにします。

実装内容：
1. UndoService クラスの作成
   - __init__(self, max_stack_size: int = 1)
   - push_state(state: AppState) -> None
   - can_undo() -> bool
   - undo() -> Optional[dict]
   - clear() -> None

2. スタック管理
   - 直前の状態を1つだけ保持（max_stack_size=1）
   - 削除操作時に現在の状態をスタックに push
   - Ctrl+Z で undo() を呼び出し

3. ログ出力
   - logger.info() でアンドゥ操作をログ

依存：
- Phase 1（models/app_state.py）完了

規約厳守事項：
- 型ヒント：すべての関数に Optional/Union/List などを明記
- Docstring：Google Style で記載
- エラー：logger.error() でコンソール出力
- コメント：Docstring と明白でない処理のみ

参考ドキュメント：
- アーキテクチャ: docs/architecture.md
- 要件定義: docs/requirements.md
- コーディング規約: docs/coding_style.md
```

### Phase 2-3: ClipboardService 実装

```markdown
【Phase 2-3: ClipboardService 実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- services/clipboard_service.py

要件：
クリップボード操作を実装してください。プロンプト本文をクリップボードにコピーします。

実装内容：
1. ClipboardService クラスの作成
   - copy_to_clipboard(page: ft.Page, text: str) -> bool
   - get_clipboard_text(page: ft.Page) -> Optional[str]

2. Flet の Clipboard API を使用
   - page.set_clipboard(text)
   - page.get_clipboard()

3. エラーハンドリング
   - コピー失敗時は False を返す
   - logger.error() でログ出力

依存：
- Flet 0.28.3 の Clipboard API

規約厳守事項：
- 型ヒント：すべての関数に Optional/Union/List などを明記
- Docstring：Google Style で記載
- Flet 0.28.3 の最新 API を使用
- エラー：logger.error() でコンソール出力

参考ドキュメント：
- Flet Clipboard API: https://flet.dev/docs/controls/page#clipboard
- コーディング規約: docs/coding_style.md
```

### Phase 2-4: SearchService 実装

```markdown
【Phase 2-4: SearchService 実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- services/search_service.py

要件：
検索・フィルタ機能を実装してください。タイトルと本文全体で検索できるようにします。

実装内容：
1. SearchService クラスの作成
   - search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]
   - filter_by_category(prompts: List[Prompt], category_ids: List[str]) -> List[Prompt]
   - filter_by_favorite(prompts: List[Prompt]) -> List[Prompt]
   - apply_filters(prompts: List[Prompt], query: str, category_ids: Optional[List[str]], favorite: bool) -> List[Prompt]

2. 検索ロジック
   - タイトルと本文の両方を対象
   - 大文字小文字を区別しない
   - 部分一致検索

3. フィルタの AND 結合
   - カテゴリフィルタと検索クエリを組み合わせ
   - お気に入りフィルタも追加可能

依存：
- Phase 1（models/prompt.py）完了

規約厳守事項：
- 型ヒント：すべての関数に Optional/Union/List などを明記
- Docstring：Google Style で記載
- コメント：Docstring と明白でない処理のみ

参考ドキュメント：
- 要件定義: docs/requirements.md
- コーディング規約: docs/coding_style.md
```

---

## Phase 3: UI スタイル定義（✅ 完了）

このフェーズは完了済みです。

---

## Phase 4: コアコンポーネント（カード表示）

### Phase 4-1: CardBody コンポーネント

```markdown
【Phase 4-1: CardBody コンポーネント実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/components/card/card_body.py

要件：
カード本文（タイトル + プレビュー）を表示するコンポーネントを実装してください。

実装内容：
1. CardBody クラス（ft.Container を継承）
   - __init__(self, title: str, body_preview: str)
   - build() -> ft.Container

2. レイアウト
   - タイトル：上部、太字、1行
   - プレビュー：下部、通常フォント、複数行可
   - utils.text_utils.truncate_preview() でプレビュー生成

3. スタイル適用
   - ui/styles/colors.py から色をインポート
   - ui/styles/typography.py からフォント定義
   - ui/styles/spacing.py から余白定義

依存：
- Phase 3（ui/styles/）完了
- utils/text_utils.py 完了

規約厳守事項：
- 型ヒント：すべての関数に ft.Control などを明記
- Docstring：Google Style で記載
- 定数：ui/styles/ から色・フォント・余白をインポート
- Flet 0.28.3 の最新 API を使用

参考ドキュメント：
- アーキテクチャ: docs/architecture.md（ui/components/card/ セクション）
- 要件定義: docs/requirements.md（カード表示）
- コーディング規約: docs/coding_style.md
```

### Phase 4-2: CardHeader コンポーネント

```markdown
【Phase 4-2: CardHeader コンポーネント実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/components/card/card_header.py

要件：
カードヘッダー（コピーボタン、お気に入り★）を表示するコンポーネントを実装してください。

実装内容：
1. CardHeader クラス（ft.Row を継承）
   - __init__(self, is_favorite: bool, on_copy: Callable, on_toggle_favorite: Callable)
   - build() -> ft.Row

2. UI 要素
   - 左側：お気に入り★アイコン（トグル可能）
   - 右側：コピーアイコンボタン
   - ft.IconButton を使用

3. イベントハンドリング
   - on_copy コールバック：コピーボタンクリック時
   - on_toggle_favorite コールバック：★クリック時

4. スタイル
   - ui/styles/colors.py から STAR_FILLED, STAR_UNFILLED
   - アイコンサイズは ui/styles/spacing.py の ICON_SIZE

依存：
- Phase 3（ui/styles/）完了

規約厳守事項：
- 型ヒント：Callable[[...], None] を明記
- Docstring：Google Style で記載
- Flet 0.28.3 の最新 API を使用
- コールバックは必ず型定義

参考ドキュメント：
- アーキテクチャ: docs/architecture.md
- 要件定義: docs/requirements.md（カード表示）
- コーディング規約: docs/coding_style.md
```

### Phase 4-3: PromptCard コンポーネント

```markdown
【Phase 4-3: PromptCard コンポーネント実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/components/card/prompt_card.py

要件：
プロンプトカード全体を組み立てるコンポーネントを実装してください。

実装内容：
1. PromptCard クラス（ft.Container を継承）
   - __init__(self, prompt: Prompt, on_click: Callable, on_copy: Callable, on_toggle_favorite: Callable)
   - build() -> ft.Container

2. コンポーネント構成
   - CardHeader（上部）
   - CardBody（中央）
   - クリック時に on_click コールバック

3. カードスタイル
   - 正方形（ui/styles/card_style.py の CARD_WIDTH, CARD_HEIGHT）
   - 背景色、ボーダー、角丸
   - ホバー時のエフェクト（透明度変更）

4. データ処理
   - utils.text_utils.truncate_preview() で本文プレビュー生成

依存：
- Phase 4-1（CardBody）完了
- Phase 4-2（CardHeader）完了

規約厳守事項：
- 型ヒント：Callable, Prompt などを明記
- Docstring：Google Style で記載
- ui/styles/card_style.py から定数インポート
- Flet 0.28.3 の最新 API を使用

参考ドキュメント：
- アーキテクチャ: docs/architecture.md
- 要件定義: docs/requirements.md（カード表示）
- コーディング規約: docs/coding_style.md
```

### Phase 4-4: CardGridView

```markdown
【Phase 4-4: CardGridView 実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/views/card_grid_view.py

要件：
カードをグリッド表示するビューを実装してください。レスポンシブに列数を調整します。

実装内容：
1. CardGridView クラス（ft.GridView を継承）
   - __init__(self, prompts: List[Prompt], on_card_click: Callable, on_copy: Callable, on_toggle_favorite: Callable)
   - build() -> ft.GridView

2. グリッドレイアウト
   - ft.GridView を使用
   - runs_count で列数を指定（画面幅に応じて調整）
   - spacing で間隔を設定

3. カードの配置
   - 各 Prompt に対して PromptCard を生成
   - on_card_click, on_copy, on_toggle_favorite をそれぞれ渡す

4. レスポンシブ対応
   - 画面幅に応じて列数を変更
   - config.py の CARD_SIZE を基準に計算

依存：
- Phase 4-3（PromptCard）完了

規約厳守事項：
- 型ヒント：List[Prompt], Callable などを明記
- Docstring：Google Style で記載
- Flet 0.28.3 の GridView API を使用
- config.py から CARD_SIZE インポート

参考ドキュメント：
- アーキテクチャ: docs/architecture.md
- 要件定義: docs/requirements.md（カード表示）
- Flet GridView: https://flet.dev/docs/controls/gridview
```

### Phase 4-5: Snackbar コンポーネント

```markdown
【Phase 4-5: Snackbar（トースト通知）実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/components/common/snackbar.py

要件：
トースト通知を表示するヘルパー関数を実装してください。

実装内容：
1. show_snackbar 関数
   - show_snackbar(page: ft.Page, message: str, duration_ms: int = 2000, bgcolor: str = None) -> None

2. Snackbar の表示
   - ft.SnackBar を使用
   - 右下に表示（控えめ）
   - 自動で消える（duration 指定）

3. メッセージタイプ
   - 成功：SUCCESS_COLOR
   - エラー：ERROR_COLOR
   - 通常：デフォルト背景色

依存：
- Phase 3（ui/styles/colors.py）完了

規約厳守事項：
- 型ヒント：ft.Page, str, int などを明記
- Docstring：Google Style で記載
- ui/styles/colors.py から色をインポート
- Flet 0.28.3 の SnackBar API を使用

参考ドキュメント：
- Flet SnackBar: https://flet.dev/docs/controls/snackbar
- コーディング規約: docs/coding_style.md
```

---

## Phase 5: 編集機能

### Phase 5-1: TitleField コンポーネント

```markdown
【Phase 5-1: TitleField コンポーネント実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/components/editor/title_field.py

要件：
タイトル入力フィールドを実装してください。

実装内容：
1. TitleField クラス（ft.TextField を継承）
   - __init__(self, value: str, on_change: Callable[[str], None])
   - build() -> ft.TextField

2. TextField の設定
   - label="タイトル"
   - hint_text="プロンプトのタイトルを入力"
   - max_length は config.TITLE_MAX_LENGTH
   - on_change イベントで親に通知

3. スタイル
   - ui/styles/typography.py からフォントサイズ
   - ui/styles/colors.py からテキスト色

依存：
- Phase 3（ui/styles/）完了

規約厳守事項：
- 型ヒント：Callable[[str], None] を明記
- Docstring：Google Style で記載
- config.py から TITLE_MAX_LENGTH をインポート
- Flet 0.28.3 の TextField API を使用

参考ドキュメント：
- アーキテクチャ: docs/architecture.md
- Flet TextField: https://flet.dev/docs/controls/textfield
```

### Phase 5-2: BodyField コンポーネント

```markdown
【Phase 5-2: BodyField コンポーネント実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/components/editor/body_field.py

要件：
本文テキストエリアを実装してください。

実装内容：
1. BodyField クラス（ft.TextField を継承）
   - __init__(self, value: str, on_change: Callable[[str], None])
   - build() -> ft.TextField

2. TextField の設定
   - label="本文"
   - multiline=True
   - min_lines=10, max_lines=20
   - on_change イベントで親に通知

3. スタイル
   - ui/styles/typography.py からフォントサイズ
   - ui/styles/colors.py からテキスト色
   - expand=True（縦に伸縮）

依存：
- Phase 3（ui/styles/）完了

規約厳守事項：
- 型ヒント：Callable[[str], None] を明記
- Docstring：Google Style で記載
- Flet 0.28.3 の TextField API を使用

参考ドキュメント：
- アーキテクチャ: docs/architecture.md
- Flet TextField: https://flet.dev/docs/controls/textfield
```

### Phase 5-3: CategorySelector コンポーネント

```markdown
【Phase 5-3: CategorySelector コンポーネント実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/components/editor/category_selector.py

要件：
カテゴリ選択 UI を実装してください。ドロップダウンまたはシンプルなリスト表示。

実装内容：
1. CategorySelector クラス（ft.Dropdown を継承）
   - __init__(self, categories: List[Category], selected_path: List[str], on_change: Callable[[List[str]], None])
   - build() -> ft.Dropdown

2. Dropdown の設定
   - label="カテゴリ"
   - options にカテゴリ一覧を表示
   - 階層表記（例："親 > 子 > 孫"）
   - on_change イベントで親に通知

3. カテゴリ階層の表現
   - フラットなリストとして表示
   - インデントまたは記号で階層を表現

依存：
- Phase 2-1（services/category_service.py）完了

規約厳守事項：
- 型ヒント：List[Category], List[str], Callable を明記
- Docstring：Google Style で記載
- Flet 0.28.3 の Dropdown API を使用

参考ドキュメント：
- アーキテクチャ: docs/architecture.md
- Flet Dropdown: https://flet.dev/docs/controls/dropdown
```

### Phase 5-4: EditorToolbar コンポーネント

```markdown
【Phase 5-4: EditorToolbar コンポーネント実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/components/editor/editor_toolbar.py

要件：
エディタツールバー（戻るボタンなど）を実装してください。

実装内容：
1. EditorToolbar クラス（ft.Row を継承）
   - __init__(self, on_back: Callable[[], None])
   - build() -> ft.Row

2. ツールバー要素
   - 左側：戻るボタン（< アイコン）
   - 右側：自動保存状態表示（オプション）

3. イベント
   - on_back コールバック：戻るボタンクリック時

4. スタイル
   - ui/styles/spacing.py から余白
   - ui/styles/colors.py から色

依存：
- Phase 3（ui/styles/）完了

規約厳守事項：
- 型ヒント：Callable[[], None] を明記
- Docstring：Google Style で記載
- Flet 0.28.3 の最新 API を使用

参考ドキュメント：
- アーキテクチャ: docs/architecture.md
```

### Phase 5-5: EditView

```markdown
【Phase 5-5: EditView 実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/views/edit_view.py

要件：
プロンプト編集ビュー全体を実装してください。自動保存機能も含めます。

実装内容：
1. EditView クラス（ft.Column を継承）
   - __init__(self, prompt: Prompt, categories: List[Category], on_save: Callable, on_back: Callable)
   - build() -> ft.Column

2. レイアウト
   - 上部：EditorToolbar
   - 中央：TitleField, BodyField, CategorySelector
   - 自動保存ロジック（デバウンス付き）

3. 自動保存
   - 入力変更後、config.AUTOSAVE_DEBOUNCE_MS ミリ秒後に保存
   - asyncio または Flet のタイマーを使用
   - on_save コールバックを呼び出し

4. イベントハンドリング
   - on_back：戻るボタンクリック時
   - on_save：自動保存時

依存：
- Phase 5-1〜5-4（すべてのエディタコンポーネント）完了

規約厳守事項：
- 型ヒント：Prompt, Callable などを明記
- Docstring：Google Style で記載
- config.py から AUTOSAVE_DEBOUNCE_MS をインポート
- Flet 0.28.3 の最新 API を使用

参考ドキュメント：
- アーキテクチャ: docs/architecture.md
- 要件定義: docs/requirements.md（編集機能）
- コーディング規約: docs/coding_style.md
```

### Phase 5-6: EditController

```markdown
【Phase 5-6: EditController 実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/controllers/edit_controller.py

要件：
編集操作のコントローラーを実装してください。

実装内容：
1. EditController クラス
   - __init__(self, prompt_service: PromptService, data_service: DataService)
   - on_save(state: AppState, prompt_id: str, title: str, body: str, category_ids: List[str]) -> None
   - on_back(on_view_change: Callable) -> None

2. 保存処理
   - prompt_service.update_prompt() を呼び出し
   - data_service.save() でデータ永続化
   - logger.info() でログ出力

3. エラーハンドリング
   - 保存失敗時は例外をキャッチ
   - logger.error() でログ出力

依存：
- Phase 2（services/prompt_service.py, data_service.py）完了
- Phase 5-5（EditView）完了

規約厳守事項：
- 型ヒント：AppState, Callable などを明記
- Docstring：Google Style で記載
- エラー：logger.error() でコンソール出力

参考ドキュメント：
- アーキテクチャ: docs/architecture.md（controllers/ セクション）
- コーディング規約: docs/coding_style.md
```

---

## Phase 6: サイドバー - カテゴリ管理

### Phase 6-1: SearchBox コンポーネント

```markdown
【Phase 6-1: SearchBox コンポーネント実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/components/sidebar/search_box.py

要件：
検索ボックスを実装してください。

実装内容：
1. SearchBox クラス（ft.TextField を継承）
   - __init__(self, on_search: Callable[[str], None])
   - build() -> ft.TextField

2. TextField の設定
   - label="検索"
   - prefix_icon=ft.icons.SEARCH
   - on_change イベント（デバウンス付き）

3. デバウンス処理
   - config.SEARCH_DEBOUNCE_MS ミリ秒後に on_search コールバック

依存：
- Phase 3（ui/styles/）完了

規約厳守事項：
- 型ヒント：Callable[[str], None] を明記
- Docstring：Google Style で記載
- config.py から SEARCH_DEBOUNCE_MS をインポート
- Flet 0.28.3 の TextField API を使用

参考ドキュメント：
- Flet TextField: https://flet.dev/docs/controls/textfield
```

### Phase 6-2: AddCategoryDialog

```markdown
【Phase 6-2: AddCategoryDialog 実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/components/dialogs/add_category_dialog.py

要件：
カテゴリ追加ダイアログを実装してください。

実装内容：
1. AddCategoryDialog クラス（ft.AlertDialog を継承）
   - __init__(self, on_add: Callable[[str, Optional[str]], None], parent_id: Optional[str] = None)
   - build() -> ft.AlertDialog

2. ダイアログ内容
   - タイトル："カテゴリを追加"
   - TextField：カテゴリ名入力
   - ボタン：追加、キャンセル

3. イベント
   - 追加ボタン：on_add コールバック（name, parent_id）
   - キャンセル：ダイアログを閉じる

4. バリデーション
   - カテゴリ名が空でないか確認
   - config.MAX_CATEGORY_NAME_LENGTH 以下か確認

依存：
- Phase 3（ui/styles/）完了

規約厳守事項：
- 型ヒント：Callable, Optional を明記
- Docstring：Google Style で記載
- config.py から MAX_CATEGORY_NAME_LENGTH をインポート
- Flet 0.28.3 の AlertDialog API を使用

参考ドキュメント：
- Flet AlertDialog: https://flet.dev/docs/controls/alertdialog
```

### Phase 6-3: AddCategoryButton

```markdown
【Phase 6-3: AddCategoryButton コンポーネント実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/components/sidebar/add_category_button.py

要件：
カテゴリ追加ボタンを実装してください。

実装内容：
1. AddCategoryButton クラス（ft.IconButton を継承）
   - __init__(self, on_click: Callable[[], None])
   - build() -> ft.IconButton

2. ボタン設定
   - icon=ft.icons.ADD
   - tooltip="カテゴリを追加"
   - on_click イベント

依存：
- Phase 3（ui/styles/）完了

規約厳守事項：
- 型ヒント：Callable[[], None] を明記
- Docstring：Google Style で記載
- Flet 0.28.3 の IconButton API を使用

参考ドキュメント：
- Flet IconButton: https://flet.dev/docs/controls/iconbutton
```

### Phase 6-4: CategoryItem（ListTile + Draggable/DragTarget）

```markdown
【Phase 6-4: CategoryItem コンポーネント実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/components/sidebar/category_item.py

要件：
カテゴリアイテム（ListTile + ドラッグ&ドロップ対応）を実装してください。

実装内容：
1. CategoryItem クラス（ft.ListTile + ft.Draggable + ft.DragTarget）
   - __init__(self, category: Category, depth: int, on_click: Callable, on_will_accept: Callable, on_accept: Callable, on_leave: Callable)
   - build() -> ft.DragTarget[ft.Draggable[ft.ListTile]]

2. ListTile 構成
   - leading: インデント + 階層記号（├ または └）
   - title: カテゴリ名（Text）
   - on_click: カテゴリ選択コールバック

3. 階層表現
   - depth 引数でインデント量を計算（depth * 20px）
   - depth=0: 記号なし、depth=1: ├、depth=2: └
   - leading_width でインデントを設定

4. ドラッグ&ドロップ
   - ft.Draggable: ドラッグ元（src_id=category.id）
   - ft.DragTarget: ドロップ先（data=category.id）
   - on_will_accept: ドロップ可否判定 + ボーダー色変更
   - on_accept: 移動処理
   - on_leave: ボーダーリセット

5. イベント
   - on_click：カテゴリ選択
   - on_will_accept：ドロップ可否チェック
   - on_accept：カテゴリ移動
   - on_leave：ボーダーリセット

依存：
- Phase 2-1（services/category_service.py）完了
- category_service.can_move_to() メソッドが実装済み

規約厳守事項：
- 型ヒント：Category, Callable などを明記
- Docstring：Google Style で記載
- Flet 0.28.3 の ListTile, Draggable, DragTarget API を使用
- 階層深さは MAX_CATEGORY_DEPTH まで

参考ドキュメント：
- Flet ListTile: https://flet.dev/docs/controls/listtile
- Flet Draggable: https://flet.dev/docs/controls/draggable
- Flet DragTarget: https://flet.dev/docs/controls/dragtarget
- 要件定義: docs/requirements.md (8.4節)
```

### Phase 6-5: CategoryTree

```markdown
【Phase 6-5: CategoryTree コンポーネント実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/components/sidebar/category_tree.py

要件：
カテゴリツリー表示を実装してください。

実装内容：
1. CategoryTree クラス（ft.Column を継承）
   - __init__(self, categories: List[Category], on_select: Callable, on_move: Callable)
   - build() -> ft.Column

2. ツリー構造
   - カテゴリを階層構造で表示
   - CategoryItem を再帰的に配置
   - 折りたたみ・展開機能（オプション）

3. イベント
   - on_select：カテゴリ選択時
   - on_move：カテゴリ移動時（D&D）

依存：
- Phase 6-4（CategoryItem）完了

規約厳守事項：
- 型ヒント：List[Category], Callable などを明記
- Docstring：Google Style で記載
- Flet 0.28.3 の最新 API を使用

参考ドキュメント：
- アーキテクチャ: docs/architecture.md
```

### Phase 6-6: Sidebar

```markdown
【Phase 6-6: Sidebar 実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/components/sidebar/sidebar.py

要件：
サイドバー全体を実装してください。

実装内容：
1. Sidebar クラス（ft.Column を継承）
   - __init__(self, categories: List[Category], on_search: Callable, on_category_select: Callable, on_category_add: Callable, on_category_move: Callable)
   - build() -> ft.Column

2. レイアウト
   - 上部：SearchBox
   - 中央：CategoryTree
   - 下部：AddCategoryButton

3. イベント処理
   - on_search：検索
   - on_category_select：カテゴリ選択
   - on_category_add：カテゴリ追加
   - on_category_move：カテゴリ移動

依存：
- Phase 6-1〜6-5（すべてのサイドバーコンポーネント）完了

規約厳守事項：
- 型ヒント：List[Category], Callable などを明記
- Docstring：Google Style で記載
- ui/styles/ から色・余白をインポート
- Flet 0.28.3 の最新 API を使用

参考ドキュメント：
- アーキテクチャ: docs/architecture.md
- 要件定義: docs/requirements.md（サイドバー）
```

### Phase 6-7: CategoryController

```markdown
【Phase 6-7: CategoryController 実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/controllers/category_controller.py

要件：
カテゴリ操作のコントローラーを実装してください。

実装内容：
1. CategoryController クラス
   - __init__(self, category_service: CategoryService, data_service: DataService)
   - on_add_category(state: AppState, name: str, parent_id: Optional[str]) -> None
   - on_move_category(state: AppState, category_id: str, new_parent_id: Optional[str]) -> None
   - on_delete_category(state: AppState, category_id: str) -> None
   - on_select_category(state: AppState, category_id: str) -> None

2. 操作処理
   - category_service のメソッドを呼び出し
   - data_service.save() でデータ永続化
   - logger.info() でログ出力

3. エラーハンドリング
   - InvalidCategoryDepthError をキャッチ
   - UI にエラーメッセージを表示（Snackbar）

依存：
- Phase 2-1（services/category_service.py）完了
- Phase 6-6（Sidebar）完了

規約厳守事項：
- 型ヒント：AppState, Optional, Callable などを明記
- Docstring：Google Style で記載
- エラー：logger.error() でコンソール出力

参考ドキュメント：
- アーキテクチャ: docs/architecture.md（controllers/ セクション）
```

---

## Phase 7: メイン画面統合

### Phase 7-1: MainView

```markdown
【Phase 7-1: MainView 実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/views/main_view.py

要件：
メイン画面全体のレイアウトを実装してください。

実装内容：
1. MainView クラス（ft.Row を継承）
   - __init__(self, state: AppState, on_view_change: Callable)
   - build() -> ft.Row

2. レイアウト
   - 左：Sidebar（20〜30% 幅）
   - 右：CardGridView または EditView（70〜80% 幅）
   - ft.Row で水平分割

3. ビュー切り替え
   - state.current_editing_id に応じて表示を切り替え
   - None：CardGridView 表示
   - 編集中：EditView 表示

依存：
- Phase 4-4（CardGridView）完了
- Phase 5-5（EditView）完了
- Phase 6-6（Sidebar）完了

規約厳守事項：
- 型ヒント：AppState, Callable などを明記
- Docstring：Google Style で記載
- Flet 0.28.3 の Row API を使用

参考ドキュメント：
- アーキテクチャ: docs/architecture.md（views/ セクション）
```

### Phase 7-2: MainController

```markdown
【Phase 7-2: MainController 実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/controllers/main_controller.py

要件：
メイン画面のコントローラーを実装してください。

実装内容：
1. MainController クラス
   - __init__(self, prompt_service, category_service, data_service, clipboard_service)
   - on_add_prompt(state: AppState) -> None
   - on_card_click(state: AppState, prompt_id: str) -> None
   - on_delete_prompt(state: AppState, prompt_id: str) -> None
   - on_copy_prompt(page: ft.Page, prompt_id: str) -> None
   - on_toggle_favorite(state: AppState, prompt_id: str) -> None
   - on_category_change(state: AppState, category_id: str) -> None
   - on_search(state: AppState, query: str) -> None

2. 操作処理
   - 各 service のメソッドを呼び出し
   - data_service.save() でデータ永続化
   - UI 更新を反映

3. エラーハンドリング
   - 例外をキャッチして Snackbar で通知
   - logger.error() でログ出力

依存：
- Phase 2（すべての services）完了
- Phase 7-1（MainView）完了

規約厳守事項：
- 型ヒント：AppState, ft.Page, Callable などを明記
- Docstring：Google Style で記載
- エラー：logger.error() でコンソール出力

参考ドキュメント：
- アーキテクチャ: docs/architecture.md（controllers/ セクション）
```

### Phase 7-3: PromptKeepApp

```markdown
【Phase 7-3: PromptKeepApp（Flet アプリケーション）実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/app.py

要件：
Flet アプリケーション全体を実装してください。

実装内容：
1. PromptKeepApp クラス
   - __init__(self)
   - run(self) -> None
   - main(self, page: ft.Page) -> None

2. 初期化
   - DataService, PromptService などのインスタンス作成
   - AppState の読み込み
   - MainController の作成

3. Page 設定
   - title="PromptKeep"
   - theme_mode="dark"
   - window_width, window_height（config から）

4. メインビューの配置
   - MainView を page.add()

依存：
- Phase 7-1（MainView）完了
- Phase 7-2（MainController）完了

規約厳守事項：
- 型ヒント：ft.Page などを明記
- Docstring：Google Style で記載
- config.py から WINDOW_WIDTH, WINDOW_HEIGHT をインポート
- Flet 0.28.3 の最新 API を使用

参考ドキュメント：
- アーキテクチャ: docs/architecture.md（ui/app.py セクション）
- Flet Page: https://flet.dev/docs/controls/page
```

### Phase 7-4: main.py 更新

```markdown
【Phase 7-4: main.py の UI 呼び出し部分を実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- main.py

要件：
main.py の TODO 部分を実装して、UI を起動できるようにしてください。

実装内容：
1. main() 関数の更新
   - ui/app.py から PromptKeepApp をインポート
   - app = PromptKeepApp() を作成
   - ft.app(target=app.main) で起動

2. コメント解除
   - 既存の TODO コメントを削除
   - PromptKeepApp の呼び出しを有効化

依存：
- Phase 7-3（PromptKeepApp）完了

規約厳守事項：
- 型ヒント：すべての関数に明記
- Docstring：Google Style で記載
- Flet 0.28.3 の ft.app() を使用

参考ドキュメント：
- Flet アプリケーション起動: https://flet.dev/docs/guides/python/getting-started
```

---

## Phase 8: ゴミ箱機能

### Phase 8-1: TrashView

```markdown
【Phase 8-1: TrashView 実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/views/trash_view.py

要件：
ゴミ箱ビュー（削除済みプロンプト一覧）を実装してください。

実装内容：
1. TrashView クラス（ft.Column を継承）
   - __init__(self, deleted_prompts: List[Prompt], on_restore: Callable, on_empty: Callable)
   - build() -> ft.Column

2. レイアウト
   - 上部：「ゴミ箱を空にする」ボタン
   - 中央：削除済みプロンプトのリスト
   - 各アイテムに「復元」ボタン

3. イベント
   - on_restore：プロンプト復元
   - on_empty：ゴミ箱を空にする（確認ダイアログ表示）

依存：
- Phase 2（services/prompt_service.py）完了

規約厳守事項：
- 型ヒント：List[Prompt], Callable などを明記
- Docstring：Google Style で記載
- Flet 0.28.3 の最新 API を使用

参考ドキュメント：
- 要件定義: docs/requirements.md（ゴミ箱機能）
```

---

## Phase 9: キーボード操作

### Phase 9-1: KeyboardController

```markdown
【Phase 9-1: KeyboardController 実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/controllers/keyboard_controller.py

要件：
キーボードショートカットを実装してください。

実装内容：
1. KeyboardController クラス
   - __init__(self, page: ft.Page, undo_service: UndoService)
   - setup_shortcuts(self) -> None
   - on_key_down(self, e: ft.KeyboardEvent) -> None

2. ショートカット
   - Ctrl+Z：アンドゥ（削除の復元）
   - その他必要に応じて追加

3. イベントハンドリング
   - page.on_keyboard_event でキーイベントを取得
   - キーの組み合わせを判定

依存：
- Phase 2-2（services/undo_service.py）完了

規約厳守事項：
- 型ヒント：ft.Page, ft.KeyboardEvent などを明記
- Docstring：Google Style で記載
- Flet 0.28.3 の KeyboardEvent API を使用

参考ドキュメント：
- Flet キーボードイベント: https://flet.dev/docs/controls/page#keyboard-events
```

---

## Phase 10: 検索・フィルタ機能

### Phase 10-1: 検索機能統合

```markdown
【Phase 10-1: 検索機能の UI 統合】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- ui/controllers/main_controller.py（on_search メソッドを拡張）

要件：
SearchService を MainController に統合し、検索機能を有効化してください。

実装内容：
1. MainController の on_search 実装
   - SearchService.search_prompts() を呼び出し
   - フィルタ結果を UI に反映

2. フィルタの組み合わせ
   - 検索クエリ + カテゴリフィルタ + お気に入りフィルタ
   - SearchService.apply_filters() を使用

依存：
- Phase 2-4（services/search_service.py）完了
- Phase 6-1（SearchBox）完了

規約厳守事項：
- 型ヒント：AppState, str などを明記
- Docstring：Google Style で記載
- エラー：logger.error() でコンソール出力

参考ドキュメント：
- 要件定義: docs/requirements.md（検索機能）
```

---

## Phase 11: エラーハンドリング・ロギング

### Phase 11-1: エラーハンドリング強化

```markdown
【Phase 11-1: 全レイヤーのエラーハンドリング強化】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- すべての services/ と controllers/ ファイル

要件：
エラーハンドリングを強化し、堅牢性を向上させてください。

実装内容：
1. 例外の適切なキャッチ
   - 各メソッドで発生しうる例外を特定
   - try-except で適切にキャッチ

2. ユーザーへのフィードバック
   - エラー時は Snackbar で通知
   - 具体的なエラーメッセージを表示

3. ログ出力
   - logger.error() でエラー内容をログ
   - logger.exception() でスタックトレースも記録

4. バックアップ・リカバリ
   - データ保存失敗時のロールバック
   - バックアップからの復元

依存：
- すべての Phase 完了

規約厳守事項：
- 型ヒント：すべての例外を明記
- Docstring：Raises セクションで例外を記載
- エラー：logger.error() または logger.exception()

参考ドキュメント：
- コーディング規約: docs/coding_style.md（エラーハンドリング）
```

---

## Phase 12: テスト・最適化

### Phase 12-1: 統合テスト・バグ修正

```markdown
【Phase 12-1: 統合テスト・バグ修正】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- すべてのファイル

要件：
全機能の統合テストを実施し、バグを修正してください。

実装内容：
1. 手動テスト
   - すべての機能を実際に操作
   - エッジケースを確認

2. バグ修正
   - 発見したバグを修正
   - ログで問題箇所を特定

3. UI/UX の微調整
   - レイアウトの調整
   - レスポンシブ対応の確認

4. パフォーマンスチューニング
   - 大量データでの動作確認
   - 不要なレンダリングを削減

依存：
- すべての Phase 完了

規約厳守事項：
- 型ヒント：維持
- Docstring：維持
- コーディング規約：すべて遵守

参考ドキュメント：
- 要件定義: docs/requirements.md
- コーディング規約: docs/coding_style.md
```

---

## 💡 テンプレート使用のコツ

1. **Phase の順番を守る**：依存関係に注意
2. **一度に1つの Phase**：複数 Phase を同時に指示しない
3. **生成後は必ず確認**：チェックリストで検証
4. **エラーが出たら**：ログを確認してテンプレートを調整

---

## 📚 次のステップ

Phase 4 から UI 実装を開始してください。
[docs/implementation_plan.md](implementation_plan.md) も併せて参照。
