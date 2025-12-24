"""検索・フィルタサービス。

プロンプトのタイトル・本文検索とカテゴリ／お気に入りフィルタを提供。
Flet 0.28.3、Python 3.14.2 対応。
"""

import logging
from typing import List, Optional

from models.prompt import Prompt

logger = logging.getLogger(__name__)


class SearchService:
    """プロンプト検索・フィルタを提供するサービス。"""

    def search_prompts(self, prompts: List[Prompt], query: str) -> List[Prompt]:
        """タイトルと本文を対象に部分一致検索する。

        大文字小文字は区別しない。空文字列の場合は入力リストをそのまま返す。

        Args:
            prompts: 検索対象のプロンプト一覧。
            query: 検索クエリ文字列。

        Returns:
            検索条件に一致するプロンプト一覧。
        """
        if not query:
            return prompts

        q = query.lower()
        return [p for p in prompts if q in p.title.lower() or q in p.body.lower()]

    def filter_by_category(
        self, prompts: List[Prompt], category_path: List[str]
    ) -> List[Prompt]:
        """カテゴリ階層でフィルタする。

        `category_path` が空なら全件を返す。指定がある場合、プロンプトの
        `category_path` が同じ長さのプレフィックスとして一致するものを返す。
        （指定カテゴリ配下の子孫カテゴリも含めてヒットさせるための前方一致）

        Args:
            prompts: フィルタ対象のプロンプト一覧。
            category_path: ルートからのカテゴリ階層。空配列で全件。

        Returns:
            カテゴリ条件に一致するプロンプト一覧。
        """
        if not category_path:
            return prompts

        length = len(category_path)
        return [p for p in prompts if p.category_path[:length] == category_path]

    def filter_by_favorite(self, prompts: List[Prompt]) -> List[Prompt]:
        """お気に入りフラグでフィルタする。

        Args:
            prompts: フィルタ対象のプロンプト一覧。

        Returns:
            お気に入りフラグが立っているプロンプト一覧。
        """
        return [p for p in prompts if p.favorite]

    def apply_filters(
        self,
        prompts: List[Prompt],
        query: str,
        category_path: Optional[List[str]],
        favorite: bool,
    ) -> List[Prompt]:
        """検索・カテゴリ・お気に入りの複合フィルタを適用する。

        フィルタは AND 条件で適用する。カテゴリは子孫を含む前方一致。

        Args:
            prompts: 対象のプロンプト一覧。
            query: 検索クエリ（空文字で無効）。
            category_path: カテゴリ階層。None/空でフィルタ無効。
            favorite: True の場合のみお気に入りで絞り込み。

        Returns:
            フィルタ適用後のプロンプト一覧。
        """
        filtered = self.search_prompts(prompts, query)
        if category_path:
            filtered = self.filter_by_category(filtered, category_path)
        if favorite:
            filtered = self.filter_by_favorite(filtered)
        return filtered
