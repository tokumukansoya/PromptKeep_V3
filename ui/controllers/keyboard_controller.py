from __future__ import annotations

import logging
from typing import Callable, Optional, Tuple

import flet as ft

from ui.components.common.snackbar import show_snackbar
from ui.styles.colors import SUCCESS_COLOR, ERROR_COLOR

logger = logging.getLogger(__name__)


class KeyboardController:
    """キーボードショートカット管理コントローラー。

    Page のキーボードイベントを監視し、ショートカット操作をハンドリングする。
    現状は Ctrl+Z により "直前に保存したスナップショットを適用する" ハンドラーを呼び出す。

    Flet 0.28.3 の KeyboardEvent API に準拠。

    Args:
        page: Flet の `Page` インスタンス。
        undo_handler: アンドゥ処理を実行するコールバック（成功/失敗メッセージ付き）。

    Attributes:
        _page: 関連付けられた `ft.Page`。
        _undo_handler: アンドゥ処理の実装を受け取るコールバック。
        _on_state_restored: UI 更新コールバック（任意）。
    """

    def __init__(
        self,
        page: ft.Page,
        undo_handler: Callable[[], Tuple[bool, str]],
        on_state_restored: Optional[Callable[[], None]] = None,
    ) -> None:
        """初期化。

        Args:
            page: Flet の `Page`。
            undo_handler: アンドゥ処理を実行するコールバック。
            on_state_restored: アンドゥ適用後に UI を更新するコールバック。
        """
        self._page: ft.Page = page
        self._undo_handler: Callable[[], Tuple[bool, str]] = undo_handler
        self._on_state_restored: Optional[Callable[[], None]] = on_state_restored
        logger.debug("KeyboardController initialized")

    def setup_shortcuts(self) -> None:
        """ショートカットのイベント購読を設定する。

        `page.on_keyboard_event` に `on_key_down()` を割り当てる。
        """
        # Flet 0.28.3: on_keyboard_event は keydown / keyup の両方を通知する
        self._page.on_keyboard_event = self.on_key_down
        logger.info("Keyboard shortcuts are set up")

    def on_key_down(self, e: ft.KeyboardEvent) -> None:
        """キーボードイベントのハンドラ。

        Args:
            e: キーボードイベント (`ft.KeyboardEvent`)。

        Note:
            - Ctrl+Z / Cmd+Z で UndoService.undo() を実行。
            - イベント種別が提供される場合（keydown/keyup）は keydown 相当のみ処理。
        """
        try:
            # 一部プラットフォームでは e.type が存在（"keydown" / "keyup"）。存在すれば keydown 相当のみ処理。
            ev_type = getattr(e, "type", None)
            if ev_type and str(ev_type).lower() == "keyup":
                return

            key = (e.key or "").lower()
            is_ctrl_or_cmd = bool(
                getattr(e, "ctrl", False) or getattr(e, "meta", False)
            )

            # Ctrl+Z / Cmd+Z => Undo
            if key == "z" and is_ctrl_or_cmd:
                success, message = self._undo_handler()
                if success:
                    if self._on_state_restored:
                        self._on_state_restored()
                    show_snackbar(self._page, message, bgcolor=SUCCESS_COLOR)
                    logger.info("Undo executed via keyboard shortcut (Ctrl+Z/Cmd+Z)")
                else:
                    show_snackbar(self._page, message, bgcolor=ERROR_COLOR)
                    logger.warning("Undo request could not be completed: %s", message)

        except Exception as ex:
            logger.exception("Failed to handle keyboard event")
            # 重大ではないため UI 通知は控えめにとどめるが、明示的に通知する
            if self._page:
                show_snackbar(
                    self._page,
                    "キーボード操作の処理に失敗しました",
                    bgcolor=ERROR_COLOR,
                )
