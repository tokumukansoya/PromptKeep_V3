"""プロンプトサービス。"""

from datetime import datetime
from typing import List, Optional

from models.prompt import Prompt


class PromptService:
    """プロンプトのCRUD操作を提供するサービス。"""

    def create_prompt(self, title: str, body: str, category_ids: Optional[List[str]] = None) -> Prompt:
        """新しいプロンプトを作成する。"""
        return Prompt.create(title=title, body=body, category_ids=category_ids)

    def update_prompt(
        self,
        prompt: Prompt,
        title: Optional[str] = None,
        body: Optional[str] = None,
        category_ids: Optional[List[str]] = None,
        favorite: Optional[bool] = None,
    ) -> Prompt:
        """プロンプトを更新する。"""
        if title is not None:
            prompt.title = title
        if body is not None:
            prompt.body = body
        if category_ids is not None:
            prompt.category_ids = category_ids
        if favorite is not None:
            prompt.favorite = favorite
        prompt.updated_at = datetime.now()
        return prompt

    def delete_prompt(self, prompt: Prompt) -> Prompt:
        """プロンプトを削除する（ゴミ箱へ移動）。"""
        prompt.deleted_at = datetime.now()
        prompt.updated_at = datetime.now()
        return prompt

    def restore_prompt(self, prompt: Prompt) -> Prompt:
        """プロンプトをゴミ箱から復元する。"""
        prompt.deleted_at = None
        prompt.updated_at = datetime.now()
        return prompt

    def toggle_favorite(self, prompt: Prompt) -> Prompt:
        """お気に入り状態をトグルする。"""
        prompt.favorite = not prompt.favorite
        prompt.updated_at = datetime.now()
        return prompt

    def search_prompts(self, prompts: List[Prompt], query: str) -> List[Prompt]:
        """プロンプトを検索する。"""
        if not query:
            return prompts
        query_lower = query.lower()
        return [
            p for p in prompts
            if query_lower in p.title.lower() or query_lower in p.body.lower()
        ]