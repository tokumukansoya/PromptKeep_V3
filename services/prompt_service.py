"""プロンプトサービス。

プロンプトの CRUD 操作を担当。
Flet 0.28.3、Python 3.14.2 対応。
"""

from datetime import datetime
from typing import List, Optional

from loguru import logger

from config import MAX_CATEGORY_DEPTH
from exceptions import (
    InvalidCategoryDepthError,
    PromptNotFoundError,
)
from models.app_state import AppState
from models.prompt import Prompt
from services.data_service import DataService


class PromptService:
    """プロンプトの CRUD 操作を提供するサービス。

    Attributes:
        data_service: データ永続化を担当するサービス。
        state: アプリケーション状態。

    Note:
        - 操作後は自動的に state が更新される。
        - 永続化は呼び出し側で実施。
    """

    def __init__(self, data_service: DataService) -> None:
        """PromptService の初期化。

        Args:
            data_service: DataService インスタンス。
        """
        self.data_service = data_service
        logger.debug("PromptService initialized")

    def create_prompt(
        self, title: str, body: str, category_ids: Optional[List[str]] = None
    ) -> Prompt:
        """新規プロンプトを作成。

        Args:
            title: プロンプトのタイトル。
            body: プロンプトの本文。
            category_ids: カテゴリIDの階層。

        Returns:
            新規作成された Prompt オブジェクト。

        Raises:
            InvalidCategoryDepthError: カテゴリ階層が深すぎる場合。
            ValidationError: バリデーション失敗時。

        Example:
            >>> service = PromptService(data_service)
            >>> prompt = service.create_prompt("タイトル", "本文")
        """
        if category_ids is None:
            category_ids = []

        if len(category_ids) > MAX_CATEGORY_DEPTH:
            logger.error(
                f"Category depth exceeds limit: {len(category_ids)} > {MAX_CATEGORY_DEPTH}"
            )
            raise InvalidCategoryDepthError(
                f"カテゴリ階層が深すぎます（最大 {MAX_CATEGORY_DEPTH}）"
            )

        prompt = Prompt.create(title, body, category_ids)
        logger.info(f"Created prompt: {prompt.id}")
        return prompt

    def get_prompt(self, state: AppState, prompt_id: str) -> Prompt:
        """ID でプロンプトを取得。

        Args:
            state: AppState オブジェクト。
            prompt_id: プロンプト ID。

        Returns:
            プロンプトオブジェクト。

        Raises:
            PromptNotFoundError: プロンプトが見つからない場合。

        Example:
            >>> service = PromptService(data_service)
            >>> prompt = service.get_prompt(state, "id123")
        """
        prompt = state.get_prompt(prompt_id)
        if prompt is None:
            logger.error(f"Prompt not found: {prompt_id}")
            raise PromptNotFoundError(f"プロンプトが見つかりません: {prompt_id}")
        return prompt

    def update_prompt(
        self,
        state: AppState,
        prompt_id: str,
        title: Optional[str] = None,
        body: Optional[str] = None,
        category_ids: Optional[List[str]] = None,
        favorite: Optional[bool] = None,
    ) -> Prompt:
        """既存プロンプトを更新。

        指定された属性のみ更新。

        Args:
            state: AppState オブジェクト。
            prompt_id: 更新対象のプロンプト ID。
            title: 新しいタイトル（未指定時は変更しない）。
            body: 新しい本文（未指定時は変更しない）。
            category_ids: 新しいカテゴリID階層（未指定時は変更しない）。
            favorite: 新しいお気に入り状態（未指定時は変更しない）。

        Returns:
            更新後のプロンプトオブジェクト。

        Raises:
            PromptNotFoundError: プロンプトが見つからない場合。
            InvalidCategoryDepthError: カテゴリ階層が深すぎる場合。

        Example:
            >>> updated = service.update_prompt(
            ...     state, "id123", title="新しいタイトル"
            ... )
        """
        prompt = self.get_prompt(state, prompt_id)

        if title is not None:
            prompt.title = title
        if body is not None:
            prompt.body = body
        if category_ids is not None:
            if len(category_ids) > MAX_CATEGORY_DEPTH:
                raise InvalidCategoryDepthError(
                    f"カテゴリ階層が深すぎます（最大 {MAX_CATEGORY_DEPTH}）"
                )
            prompt.category_ids = category_ids
        if favorite is not None:
            prompt.favorite = favorite

        prompt.updated_at = datetime.now()
        logger.info(f"Updated prompt: {prompt_id}")
        return prompt

    def delete_prompt(self, state: AppState, prompt_id: str) -> None:
        """プロンプトを削除（論理削除）。

        ゴミ箱に移動。

        Args:
            state: AppState オブジェクト。
            prompt_id: 削除対象のプロンプト ID。

        Raises:
            PromptNotFoundError: プロンプトが見つからない場合。

        Example:
            >>> service.delete_prompt(state, "id123")
        """
        prompt = self.get_prompt(state, prompt_id)

        prompt.deleted_at = datetime.now()
        if prompt_id not in state.trash:
            state.trash.append(prompt_id)

        logger.info(f"Deleted prompt: {prompt_id}")

    def restore_prompt(self, state: AppState, prompt_id: str) -> None:
        """削除したプロンプトを復元。

        ゴミ箱から戻す。

        Args:
            state: AppState オブジェクト。
            prompt_id: 復元対象のプロンプト ID。

        Raises:
            PromptNotFoundError: プロンプトが見つからない場合。

        Example:
            >>> service.restore_prompt(state, "id123")
        """
        prompt = self.get_prompt(state, prompt_id)

        prompt.deleted_at = None
        if prompt_id in state.trash:
            state.trash.remove(prompt_id)

        logger.info(f"Restored prompt: {prompt_id}")

    def list_active_prompts(self, state: AppState) -> List[Prompt]:
        """削除されていないプロンプトを取得。

        Args:
            state: AppState オブジェクト。

        Returns:
            アクティブなプロンプトリスト。

        Example:
            >>> prompts = service.list_active_prompts(state)
        """
        return state.get_active_prompts()

    def list_deleted_prompts(self, state: AppState) -> List[Prompt]:
        """削除されたプロンプトを取得（ゴミ箱用）。

        Args:
            state: AppState オブジェクト。

        Returns:
            削除済みプロンプトリスト。

        Example:
            >>> deleted = service.list_deleted_prompts(state)
        """
        return state.get_deleted_prompts()

    def permanently_delete_prompt(self, state: AppState, prompt_id: str) -> None:
        """プロンプトを完全削除。

        ゴミ箱からも削除。

        Args:
            state: AppState オブジェクト。
            prompt_id: 完全削除対象のプロンプト ID。

        Raises:
            PromptNotFoundError: プロンプトが見つからない場合。

        Example:
            >>> service.permanently_delete_prompt(state, "id123")
        """
        prompt = self.get_prompt(state, prompt_id)

        state.prompts.remove(prompt)
        if prompt_id in state.trash:
            state.trash.remove(prompt_id)

        logger.info(f"Permanently deleted prompt: {prompt_id}")

    def empty_trash(self, state: AppState) -> None:
        """ゴミ箱を空にする。

        Args:
            state: AppState オブジェクト。

        Example:
            >>> service.empty_trash(state)
        """
        deleted_ids = state.trash.copy()
        for prompt_id in deleted_ids:
            self.permanently_delete_prompt(state, prompt_id)

        logger.info(f"Emptied trash: {len(deleted_ids)} prompts")

    def toggle_favorite(self, state: AppState, prompt_id: str) -> None:
        """プロンプトのお気に入り状態をトグル。

        Args:
            state: AppState オブジェクト。
            prompt_id: 対象のプロンプト ID。

        Raises:
            PromptNotFoundError: プロンプトが見つからない場合。

        Example:
            >>> service.toggle_favorite(state, "id123")
        """
        prompt = self.get_prompt(state, prompt_id)
        prompt.favorite = not prompt.favorite
        prompt.updated_at = datetime.now()
        logger.info(f"Toggled favorite for prompt: {prompt_id} -> {prompt.favorite}")
