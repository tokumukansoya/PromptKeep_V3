from __future__ import annotations

import logging
from typing import Callable, List

from models.app_state import AppState
from services.prompt_service import PromptService
from services.data_service import DataService

logger = logging.getLogger(__name__)


class EditController:
    """編集操作を扱うコントローラー。

    Prompt の更新（保存）と、編集ビューからの戻り遷移を担当する。
    """

    def __init__(
        self, prompt_service: PromptService, data_service: DataService
    ) -> None:
        """EditController の初期化。

        Args:
            prompt_service: プロンプトの CRUD を提供するサービス。
            data_service: データ永続化を担当するサービス。
        """
        self._prompt_service = prompt_service
        self._data_service = data_service
        logger.debug("EditController initialized")

    def on_save(
        self,
        state: AppState,
        prompt_id: str,
        title: str,
        body: str,
        category_path: List[str],
    ) -> None:
        """編集内容を保存する。

        Prompt を更新し、AppState を永続化する。

        Args:
            state: 現在のアプリケーション状態。
            prompt_id: 更新対象のプロンプト ID。
            title: 新しいタイトル。
            body: 新しい本文。
            category_path: 新しいカテゴリ階層。

        Returns:
            None

        Raises:
            例外は捕捉してログ出力し、ここでは再送出しない。
        """
        try:
            self._prompt_service.update_prompt(
                state,
                prompt_id,
                title=title,
                body=body,
                category_path=category_path,
            )
            self._data_service.save(state)
            logger.info("Prompt saved: %s", prompt_id)
        except Exception as e:
            logger.error("Failed to save prompt '%s': %s", prompt_id, e)

    def on_back(self, on_view_change: Callable[[], None]) -> None:
        """編集ビューから戻る遷移を実行する。

        Args:
            on_view_change: ビュー切り替えのコールバック（戻り先へ遷移）。

        Returns:
            None
        """
        try:
            on_view_change()
            logger.debug("Back navigation from EditView executed")
        except Exception as e:
            logger.error("Failed to navigate back from EditView: %s", e)
