from __future__ import annotations

import logging
from typing import Optional

import flet as ft

from services.undo_service import UndoService
from ui.components.common.snackbar import show_snackbar
from ui.styles.colors import SUCCESS_COLOR, ERROR_COLOR

logger = logging.getLogger(__name__)


class KeyboardController:
    """キーボードショートカット管理コントローラー。

    Page のキーボードイベントを監視し、ショートカット操作をハンドリングする。
    現状は Ctrl+Z により `UndoService.undo()` を呼び出す。

    Flet 0.28.3 の KeyboardEvent API に準拠。

    Args:
        page: Flet の `Page` インスタンス。
        undo_service: アンドゥ管理の `UndoService`。

    Attributes:
        _page: 関連付けられた `ft.Page`。
        _undo_service: `UndoService` の参照。
    """

    def __init__(self, page: ft.Page, undo_service: UndoService) -> None:
        """初期化。

        Args:
            page: Flet の `Page`。
            undo_service: アンドゥ管理の `UndoService`。
        """
        self._page: ft.Page = page
        self._undo_service: UndoService = undo_service
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
                snapshot = self._undo_service.undo()
                if snapshot is None:
                    show_snackbar(
                        self._page, "元に戻せる操作がありません", bgcolor=ERROR_COLOR
                    )
                    logger.warning("Undo requested but nothing to undo")
                    return

                # ここでは snapshot を呼び出し側で適用する設計（Phase 2-2 仕様）
                show_snackbar(self._page, "元に戻しました", bgcolor=SUCCESS_COLOR)
                logger.info("Undo executed via keyboard shortcut (Ctrl+Z/Cmd+Z)")

                # 呼び出し側が snapshot を取得して適用できるように、ページのセッションに一時保存する選択肢もある。
                # ただし本実装では副作用を避け、通知のみ行う。

        except Exception as ex:
            logger.error(f"Failed to handle keyboard event: {ex}")
            # 重大ではないため UI 通知は控えめにとどめる
