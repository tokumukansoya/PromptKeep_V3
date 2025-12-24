from __future__ import annotations

from typing import Callable

import flet as ft

from config import TITLE_MAX_LENGTH
from ui.styles import colors, typography


class TitleField(ft.TextField):
    """タイトル入力用テキストフィールド。

    Flet 0.28.3 の TextField を継承し、タイトル入力に必要な既定設定を適用する。
    """

    def __init__(self, value: str, on_change: Callable[[str], None]) -> None:
        """初期化。

        Args:
            value: 初期表示するタイトル文字列。
            on_change: 値変更時にタイトル文字列を受け取るコールバック。
        """
        super().__init__()
        self._on_change: Callable[[str], None] = on_change

        # 表示・バリデーション設定
        self.value = value
        self.label = "タイトル"
        self.hint_text = "プロンプトのタイトルを入力"
        self.max_length = TITLE_MAX_LENGTH

        # スタイル
        self.text_size = typography.FONT_SIZE_TITLE
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
