from __future__ import annotations

from typing import Callable

import flet as ft


class AddCategoryButton(ft.IconButton):
    """カテゴリ追加ボタン。

    ユーザーのクリックに応じてコールバックを呼び出します。

    Args:
        on_click: ボタンがクリックされた際に呼び出されるコールバック。
    """

    def __init__(self, on_click: Callable[[], None]) -> None:
        """初期化。

        Args:
            on_click: ボタンがクリックされた際に呼び出されるコールバック。
        """
        super().__init__(
            icon=ft.icons.ADD,
            tooltip="カテゴリを追加",
            on_click=self._handle_click,
        )
        self._on_click: Callable[[], None] = on_click

    def _handle_click(self, _: ft.ControlEvent) -> None:
        """クリックイベント。"""
        self._on_click()

    def build(self) -> ft.IconButton:  # type: ignore[override]
        """Flet ビルド関数。

        Returns:
            IconButton: 自身のインスタンスを返します。
        """
        return self
