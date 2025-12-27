# Flet 0.28.3 機能互換性チェックリスト

## 📋 調査完了日: 2025-12-27

このドキュメントは、PromptKeepの要件とFlet 0.28.3の機能互換性を検証した結果をまとめたものです。

---

## ✅ 完全に実装可能な機能

### 1. **TextField（テキスト入力）**
**要件:**
- タイトル入力（1行）
- 本文入力（複数行、min_lines=10）
- 検索ボックス

**Flet対応状況:** ✅ 完全対応
- `ft.TextField(multiline=False)` - 1行入力
- `ft.TextField(multiline=True, min_lines=10)` - 複数行入力
- `on_change` イベントで自動保存対応可能
- `on_submit` イベントでEnterキー対応

**参考:** https://flet.dev/docs/controls/textfield

---

### 2. **SnackBar（通知）**
**要件:**
- 右下に2〜3秒表示
- メッセージ例：「コピーしました」「削除しました」「復元しました」

**Flet対応状況:** ✅ 完全対応
- `ft.SnackBar(content=ft.Text("メッセージ"), duration=2000)`
- `page.open(snackbar)` で表示
- `duration` プロパティで表示時間制御可能（ミリ秒単位）
- `behavior=SnackBarBehavior.FLOATING` で位置調整可能

**参考:** https://flet.dev/docs/controls/snackbar

---

### 3. **Dropdown（カテゴリ選択）**
**要件:**
- カテゴリ選択ドロップダウン（編集ビュー内）
- 階層表示が必要

**Flet対応状況:** ✅ 対応可能（工夫が必要）
- `ft.Dropdown` が存在
- **階層表示の制限**: Dropdownは平坦なリストのみサポート
- **回避策**: カテゴリ名にインデント記号を付けて階層を表現
  ```python
  ft.Dropdown(
      options=[
          ft.dropdown.Option("root1", "カテゴリ1"),
          ft.dropdown.Option("child1-1", "  ├ サブカテゴリ1-1"),
          ft.dropdown.Option("child1-2", "  └ サブカテゴリ1-2"),
      ]
  )
  ```

**推奨:** ドキュメント更新不要（現在の仕様で対応可能）

---

### 4. **AlertDialog（ダイアログ）**
**要件:**
- カテゴリ追加ダイアログ（名前入力 + 親カテゴリ選択）
- 確認ダイアログ（汎用）

**Flet対応状況:** ✅ 完全対応
- `ft.AlertDialog` が使用可能
- モーダル表示、タイトル、コンテンツ、アクションボタンをサポート
- 使用例:
  ```python
  dialog = ft.AlertDialog(
      title=ft.Text("カテゴリ追加"),
      content=ft.Column([
          ft.TextField(label="カテゴリ名"),
          ft.Dropdown(label="親カテゴリ", options=[...])
      ]),
      actions=[
          ft.TextButton("キャンセル", on_click=close_dialog),
          ft.TextButton("作成", on_click=create_category)
      ]
  )
  page.open(dialog)
  ```

**参考:** https://flet.dev/docs/controls/alertdialog

---

### 5. **Clipboard API（クリップボード）**
**要件:**
- `page.set_clipboard(text)` - コピー
- `page.get_clipboard()` - 取得（将来的に使用可能性あり）

**Flet対応状況:** ✅ 完全対応
- Pageオブジェクトにクリップボードメソッドが存在
- 確認済み（Flet 0.28.3公式ドキュメント）

---

### 6. **キーボードイベント（Ctrl+Z など）**
**要件:**
- Ctrl+Z: アンドゥ（削除の復元）
- Ctrl+C: コピー（任意）
- Ctrl+F: 検索フォーカス（任意）

**Flet対応状況:** ✅ 完全対応
- `page.on_keyboard_event` イベントが利用可能
- `KeyboardEvent` オブジェクトでキー判定
- 使用例:
  ```python
  def on_keyboard(e: ft.KeyboardEvent):
      if e.key == "Z" and e.ctrl:
          undo_service.undo()
      page.update()
  
  page.on_keyboard_event = on_keyboard
  ```

**参考:** https://flet.dev/docs/controls/page#on_keyboard_event

---

### 7. **GridView（正方形カード）**
**要件:**
- 正方形カード（200x200px）
- レスポンシブに列数調整

**Flet対応状況:** ✅ 完全対応
- `ft.GridView(child_aspect_ratio=1.0)` で正方形を実現
- `max_extent=200` でサイズ制限
- `runs_count` または `max_extent` で列数自動調整

**確認済み（前回調査）**

---

### 8. **レスポンシブレイアウト**
**要件:**
- ウィンドウサイズ変更に対応
- GridViewの列数自動調整
- サイドバーの折りたたみ（任意）

**Flet対応状況:** ✅ 対応可能
- `page.on_resized` イベントでウィンドウサイズ変更を検知
- `page.width` / `page.height` で現在のサイズ取得
- GridViewの`runs_count`を動的に変更可能
- 使用例:
  ```python
  def on_resize(e):
      new_cols = max(1, int(page.width / 220))  # カード幅200px+余白20px
      grid_view.runs_count = new_cols
      page.update()
  
  page.on_resized = on_resize
  ```

**推奨:** requirements.mdに追記

---

### 9. **ビュー切り替え（カードグリッド ↔ 編集ビュー）**
**要件:**
- 右ペインでカードグリッドと編集ビューを切り替え

**Flet対応状況:** ✅ 対応可能（複数パターン）

**パターン1: visible プロパティ**
```python
card_grid_view.visible = True
edit_view.visible = False
page.update()
```

**パターン2: Stack + visible**
```python
ft.Stack([
    card_grid_view,
    edit_view  # visible=Falseで非表示
])
```

**パターン3: 動的に controls を置き換え**
```python
right_pane.controls = [edit_view]
page.update()
```

**推奨:** パターン1（シンプル）

---

## ⚠️ 実装に工夫が必要な機能

### 10. **Dropdown階層表示**
**問題:** Dropdownは平坦なリストのみサポート、TreeView的な階層表示不可

**回避策:** インデント記号（├ └）で視覚的に階層を表現
```python
ft.Dropdown(
    options=[
        ft.dropdown.Option("root", "仕事"),
        ft.dropdown.Option("c1", "  ├ プロジェクトA"),
        ft.dropdown.Option("c2", "  └ プロジェクトB"),
    ]
)
```

**ドキュメント影響:** なし（現在の仕様で対応可能）

---

## ❌ Flet 0.28.3で直接サポートされていない機能

### 11. **TreeView（カテゴリツリー表示）**
**問題:** `ft.TreeView` コントロールが存在しない

**解決済み:** ListTile + Draggable/DragTarget で実装（前回対応完了）

---

## 🔧 実装上の注意点

### 非同期処理（asyncio）
**問題:** `asyncio.create_task()` を直接使うとFletのイベントループと競合

**解決策:** `page.run_task()` を使用（ASYNC_GUIDELINES.md参照）
- ✅ 修正完了（requirements.md, architecture.md）

---

### ファイルI/O（JSON保存）
**Flet制限:** なし
- Python標準の`json`モジュールを使用可能
- 同期的なファイル操作で問題なし

---

### ウィンドウサイズ設定
**要件:** WINDOW_WIDTH = 1200, WINDOW_HEIGHT = 800

**Flet対応:**
```python
page.window.width = 1200
page.window.height = 800
page.update()
```

**参考:** https://flet.dev/docs/controls/page#window

---

## 📊 総合評価

| カテゴリ | 機能数 | 完全対応 | 工夫必要 | 対応不可 |
|---------|-------|---------|---------|---------|
| UI入力 | 3 | 3 | 0 | 0 |
| 通知・ダイアログ | 2 | 2 | 0 | 0 |
| レイアウト | 4 | 4 | 0 | 0 |
| イベント | 2 | 2 | 0 | 0 |
| カテゴリUI | 2 | 0 | 2 | 0 |
| **合計** | **13** | **11** | **2** | **0** |

**対応率: 100%**（全機能が何らかの形で実装可能）

---

## 🎯 結論

**すべての要件がFlet 0.28.3で実装可能です。**

- ✅ **完全対応**: TextField, SnackBar, AlertDialog, Clipboard, Keyboard, GridView, レスポンシブ、ビュー切り替え
- ⚠️ **工夫必要**: Dropdown階層表示、TreeView代替（ListTile実装済み）
- ❌ **対応不可**: なし

**追加ドキュメント更新が必要な項目:**
- requirements.mdにレスポンシブ対応の詳細を追記（推奨）

---

## 📚 参考資料

- Flet 0.28.3 公式ドキュメント: https://flet.dev/docs
- PromptKeep設計ドキュメント:
  - [requirements.md](requirements.md)
  - [architecture.md](architecture.md)
  - [ASYNC_GUIDELINES.md](ASYNC_GUIDELINES.md) - 非同期処理ガイド
  - [DESIGN_IMPROVEMENTS.md](DESIGN_IMPROVEMENTS.md) - 設計改善記録

---

**最終更新**: 2025-12-27  
**調査担当**: AI（GitHub Copilot）
