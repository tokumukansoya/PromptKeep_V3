"""プロンプトサービス。

プロンプトのCRUD操作を提供するビジネスロジック層。
"""

from datetime import datetime
from typing import List, Optional

from models.prompt import Prompt


class PromptService:
    """プロンプトのCRUD操作を提供するサービス。

    データの永続化はStateManager経由で行う。
    このクラスはビジネスロジックのみを担当する。
    """

    def create_prompt(
        self,
        title: str,
        body: str,
        category_ids: Optional[List[str]] = None,
    ) -> Prompt:
        """新しいプロンプトを作成する。

        Args:
            title: プロンプトのタイトル
            body: プロンプトの本文
            category_ids: 所属カテゴリIDのリスト

        Returns:
            作成されたプロンプト
        """
        return Prompt.create(title=title, body=body, category_ids=category_ids)

    def update_prompt(
        self,
        prompt: Prompt,
        title: Optional[str] = None,
        body: Optional[str] = None,
        category_ids: Optional[List[str]] = None,
        favorite: Optional[bool] = None,
    ) -> Prompt:
        """プロンプトを更新する。

        Args:
            prompt: 更新対象のプロンプト
            title: 新しいタイトル（Noneの場合は更新しない）
            body: 新しい本文（Noneの場合は更新しない）
            category_ids: 新しいカテゴリIDリスト（Noneの場合は更新しない）
            favorite: 新しいお気に入り状態（Noneの場合は更新しない）

        Returns:
            更新されたプロンプト
        """
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
        """プロンプトを削除する（ゴミ箱へ移動）。

        Args:
            prompt: 削除するプロンプト

        Returns:
            削除済みのプロンプト
        """
        prompt.deleted_at = datetime.now()
        prompt.updated_at = datetime.now()
        return prompt

    def restore_prompt(self, prompt: Prompt) -> Prompt:
        """プロンプトをゴミ箱から復元する。

        Args:
            prompt: 復元するプロンプト

        Returns:
            復元されたプロンプト
        """
        prompt.deleted_at = None
        prompt.updated_at = datetime.now()
        return prompt

    def toggle_favorite(self, prompt: Prompt) -> Prompt:
        """お気に入り状態をトグルする。

        Args:
            prompt: トグルするプロンプト

        Returns:
            更新されたプロンプト
        """
        prompt.favorite = not prompt.favorite
        prompt.updated_at = datetime.now()
        return prompt

    def search_prompts(self, prompts: List[Prompt], query: str) -> List[Prompt]:
        """プロンプトを検索する。

        タイトルまたは本文にクエリ文字列が含まれるプロンプトを返す。
        検索は大文字・小文字を区別しない。

        Args:
            prompts: 検索対象のプロンプトリスト
            query: 検索クエリ

        Returns:
            マッチしたプロンプトのリスト
        """
        if not query:
            return prompts
        query_lower = query.lower()
        return [
            p for p in prompts
            if query_lower in p.title.lower() or query_lower in p.body.lower()
        ]