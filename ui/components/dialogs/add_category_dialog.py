from __future__ import annotations

from typing import Callable, Optional

import flet as ft

from config import MAX_CATEGORY_NAME_LENGTH
from ui.styles import colors, spacing


class AddCategoryDialog(ft.AlertDialog):
    """カテゴリ追加ダイアログ。

    カテゴリ名の入力を受け取り、バリデーション通過後に
    コールバックへ `name` と `parent_id` を渡します。

    Args:
        on_add: 追加確定時に呼び出すコールバック。`(name, parent_id)` を渡す。
        parent_id: 追加先の親カテゴリ ID。ルート追加時は `None`。
    """

    def __init__(
        self,
        on_add: Callable[[str, Optional[str]], None],
        parent_id: Optional[str] = None,
    ) -> None:
        """初期化。

        Args:
            on_add: 追加確定時に呼び出すコールバック。`(name, parent_id)` を渡す。
            parent_id: 追加先の親カテゴリ ID。ルート追加時は `None`。
        """
        super().__init__()

        self._on_add: Callable[[str, Optional[str]], None] = on_add
        self._parent_id: Optional[str] = parent_id

        # タイトル
        self.title = ft.Text(
            value="カテゴリを追加",
            color=colors.TEXT_PRIMARY,
            size=spacing.ICON_SIZE,
        )

        # 入力フィールド
        self._name_field = ft.TextField(
            label="カテゴリ名",
            autofocus=True,
            on_change=self._clear_error,
        )

        # コンテンツ
        self.content = ft.Column(
            controls=[self._name_field],
            spacing=spacing.GAP_MD,
            tight=True,
        )

        # アクションボタン
        add_button = ft.TextButton(text="追加", on_click=self._handle_add)
        cancel_button = ft.TextButton(text="キャンセル", on_click=self._handle_cancel)
        self.actions = [add_button, cancel_button]

        # ダイアログの見た目調整（必要に応じて）
        self.modal = True

    def _clear_error(self, _: ft.ControlEvent) -> None:
        """入力変更時にエラー表示をクリアする。"""
        if self._name_field.error_text:
            self._name_field.error_text = None
            if self.page:
                self.page.update()

    def _handle_add(self, _: ft.ControlEvent) -> None:
        """追加ボタンのクリックイベント。バリデーション後にコールバックを呼び出す。"""
        name = (self._name_field.value or "").strip()

        # バリデーション: 空チェック
        if not name:
            self._name_field.error_text = "カテゴリ名を入力してください"
            if self.page:
                self.page.update()
            return

        # バリデーション: 最大長チェック
        if len(name) > MAX_CATEGORY_NAME_LENGTH:
            self._name_field.error_text = (
                f"{MAX_CATEGORY_NAME_LENGTH}文字以内で入力してください"
            )
            if self.page:
                self.page.update()
            return

        # コールバック呼び出し
        self._on_add(name, self._parent_id)

        # ダイアログを閉じる
        self.open = False
        if self.page:
            self.page.update()

    def _handle_cancel(self, _: ft.ControlEvent) -> None:
        """キャンセルボタンのクリックイベント。ダイアログを閉じる。"""
        self.open = False
        if self.page:
            self.page.update()

    def build(self) -> ft.AlertDialog:  # type: ignore[override]
        """Flet ビルド関数。

        Returns:
            AlertDialog: 自身のインスタンスを返します。
        """
        return self
