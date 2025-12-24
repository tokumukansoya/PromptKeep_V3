from __future__ import annotations

from typing import Callable, Optional

import threading

import flet as ft
from config import SEARCH_DEBOUNCE_MS


class SearchBox(ft.TextField):
    """検索ボックスコンポーネント。

    ユーザーの入力を一定時間デバウンスし、確定された検索語句を
    コールバックに渡します。

    Args:
        on_search: デバウンス後に検索語句を受け取るコールバック。
    """

    def __init__(self, on_search: Callable[[str], None]) -> None:
        """初期化。

        Args:
            on_search: デバウンス後に検索語句を受け取るコールバック。
        """
        super().__init__(
            label="検索",
            prefix_icon="search",
        )
        self._on_search: Callable[[str], None] = on_search
        self._debounce_timer: Optional[threading.Timer] = None

        # 変更イベントハンドラを登録（デバウンス処理を実施）
        self.on_change = self._handle_change

    def _handle_change(self, _: ft.ControlEvent) -> None:
        """テキスト変更イベント（デバウンス処理付き）。

        入力のたびにタイマーをリセットし、一定時間後に現在の入力値で
        検索コールバックを呼び出します。
        """
        if self._debounce_timer is not None:
            self._debounce_timer.cancel()
            self._debounce_timer = None

        # 現在の値をキャプチャして、タイマー完了時に検索を実行
        current_value = self.value or ""
        delay_sec = SEARCH_DEBOUNCE_MS / 1000.0
        self._debounce_timer = threading.Timer(
            delay_sec, self._fire_search, args=(current_value,)
        )
        self._debounce_timer.daemon = True
        self._debounce_timer.start()

    def _fire_search(self, query: str) -> None:
        """デバウンス完了時に検索コールバックを呼び出す。

        Args:
            query: 確定された検索語句。
        """
        self._on_search(query)

    def build(self) -> ft.TextField:  # type: ignore[override]
        """Flet ビルド関数。

        Returns:
            TextField: 自身のインスタンスを返します。
        """
        return self
