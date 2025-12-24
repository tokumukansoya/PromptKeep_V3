from __future__ import annotations

from typing import Callable

import flet as ft

from ui.styles import colors, typography


class BodyField(ft.TextField):
    """本文入力用のテキストエリア。"""

    def __init__(self, value: str, on_change: Callable[[str], None]) -> None:
        """初期化。

        Args:
            value: 初期表示する本文文字列。
            on_change: 値変更時に本文文字列を受け取るコールバック。
        """
        super().__init__()
        self._on_change: Callable[[str], None] = on_change

        # フィールド設定
        self.value = value
        self.label = "本文"
        self.multiline = True
        self.min_lines = 10
        self.max_lines = 20
        self.expand = True

        # スタイル
        self.text_size = typography.FONT_SIZE_BODY
        self.color = colors.TEXT_PRIMARY

        # イベント
        self.on_change = self._handle_change

    def _handle_change(self, e: ft.ControlEvent) -> None:
        """値変更時に親へ文字列を通知する。"""
        new_value = e.control.value if e.control and e.control.value is not None else ""
        self._on_change(str(new_value))

    def build(self) -> ft.TextField:  # type: ignore[override]
        """Flet ビルド関数。"""
        return self
