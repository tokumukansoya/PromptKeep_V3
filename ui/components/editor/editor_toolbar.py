from __future__ import annotations

from typing import Callable

import flet as ft

from ui.styles import colors, spacing


class EditorToolbar(ft.Row):
    """エディタ画面上部のツールバー。"""

    def __init__(self, on_back: Callable[[], None]) -> None:
        """初期化。

        Args:
            on_back: 戻るボタンクリック時に呼ばれるコールバック。
        """
        super().__init__()
        self._on_back: Callable[[], None] = on_back

        back_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
            tooltip="戻る",
            icon_color=colors.TEXT_PRIMARY,
            icon_size=spacing.ICON_SIZE,
            on_click=self._handle_back,
        )

        autosave_status = ft.Row(
            controls=[
                ft.Icon(
                    name=ft.icons.SAVE_ALT_ROUNDED,
                    size=spacing.ICON_SIZE,
                    color=colors.TEXT_SECONDARY,
                ),
                ft.Text(
                    value="自動保存",
                    color=colors.TEXT_SECONDARY,
                    size=spacing.ICON_SIZE,  # reuse icon size as text size for consistency
                ),
            ],
            spacing=spacing.GAP_XS,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.controls = [
            back_button,
            ft.Container(expand=True),
            autosave_status,
        ]
        self.alignment = ft.MainAxisAlignment.START
        self.spacing = spacing.GAP_MD
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.padding = ft.padding.only(
            left=spacing.PADDING_SM,
            right=spacing.PADDING_SM,
            top=spacing.PADDING_SM,
            bottom=spacing.PADDING_SM,
        )

    def _handle_back(self, _: ft.ControlEvent) -> None:
        """戻るボタンのクリックイベント。"""
        self._on_back()

    def build(self) -> ft.Row:  # type: ignore[override]
        """Flet ビルド関数。"""
        return self
