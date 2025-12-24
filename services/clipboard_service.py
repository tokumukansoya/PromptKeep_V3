"""クリップボードサービス。

Flet の Clipboard API を利用してテキストのコピー/取得を提供する。
Flet 0.28.3、Python 3.14.2 対応。
"""

import logging
from typing import Optional

import flet as ft

logger = logging.getLogger(__name__)


class ClipboardService:
    """クリップボード操作を提供するサービス。"""

    def copy_to_clipboard(self, page: ft.Page, text: str) -> bool:
        """テキストをクリップボードにコピーする。

        Args:
            page: Flet の `Page` インスタンス。
            text: クリップボードへコピーする文字列。

        Returns:
            コピーが成功した場合は True、失敗した場合は False。
        """
        try:
            page.set_clipboard(text)
            return True
        except Exception as e:  # noqa: BLE001
            logger.error("Failed to copy to clipboard: %s", e)
            return False

    def get_clipboard_text(self, page: ft.Page) -> Optional[str]:
        """クリップボードのテキストを取得する。

        Args:
            page: Flet の `Page` インスタンス。

        Returns:
            取得したテキスト。失敗時や未設定時は None。
        """
        try:
            return page.get_clipboard()
        except Exception as e:  # noqa: BLE001
            logger.error("Failed to get clipboard text: %s", e)
            return None
