"""アプリケーション状態モデル。

アプリケーション全体の状態を保持し、フィルタリングヘルパーを提供する。
"""

from dataclasses import dataclass, field
from typing import List, Optional

from models.prompt import Prompt
from models.category import Category


@dataclass
class AppState:
    """アプリケーション全体の状態を保持するデータクラス。

    Attributes:
        prompts: プロンプトのリスト
        categories: カテゴリのリスト
        selected_category_id: 選択中のカテゴリID
        search_query: 検索クエリ
        current_editing_id: 編集中のプロンプトID
    """

    prompts: List[Prompt] = field(default_factory=list)
    categories: List[Category] = field(default_factory=list)
    trash_prompt_ids: List[str] = field(default_factory=list)
    trash_category_ids: List[str] = field(default_factory=list)
    selected_category_id: Optional[str] = None
    search_query: str = ""
    current_editing_id: Optional[str] = None

    @classmethod
    def empty(cls) -> "AppState":
        """空の AppState を作成する。"""
        return cls()

    def to_dict(self) -> dict:
        """辞書に変換する（永続化用）。"""
        return {
            "prompts": [p.to_dict() for p in self.prompts],
            "categories": [c.to_dict() for c in self.categories],
            "trash": {
                "prompts": self.trash_prompt_ids,
                "categories": self.trash_category_ids,
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AppState":
        """辞書から AppState を作成する。
        
        Args:
            data: 状態データの辞書
            
        Returns:
            AppState インスタンス
        """
        try:
            prompts = [Prompt.from_dict(p) for p in data.get("prompts", [])]
        except Exception:
            prompts = []
        
        try:
            categories = [Category.from_dict(c) for c in data.get("categories", [])]
        except Exception:
            categories = []
        
        trash = data.get("trash", {})
        return cls(
            prompts=prompts,
            categories=categories,
            trash_prompt_ids=trash.get("prompts", []) if isinstance(trash, dict) else [],
            trash_category_ids=trash.get("categories", []) if isinstance(trash, dict) else [],
        )

    def get_active_prompts(self) -> List[Prompt]:
        """削除されていないプロンプトを取得する。"""
        return [p for p in self.prompts if p.deleted_at is None]

    def get_trashed_prompts(self) -> List[Prompt]:
        """ゴミ箱にあるプロンプトを取得する。"""
        return [p for p in self.prompts if p.deleted_at is not None]

    def get_favorite_prompts(self) -> List[Prompt]:
        """お気に入りのプロンプトを取得する。"""
        return [p for p in self.get_active_prompts() if p.favorite]

    def get_prompts_by_category(self, category_id: str) -> List[Prompt]:
        """特定のカテゴリに属するプロンプトを取得する。"""
        return [p for p in self.get_active_prompts() if category_id in p.category_ids]

    def get_uncategorized_prompts(self) -> List[Prompt]:
        """カテゴリなしのプロンプトを取得する。"""
        return [p for p in self.get_active_prompts() if not p.category_ids]

    def get_category_by_id(self, category_id: str) -> Optional[Category]:
        """IDでカテゴリを取得する。"""
        for c in self.categories:
            if c.id == category_id:
                return c
        return None

    def get_prompt_by_id(self, prompt_id: str) -> Optional[Prompt]:
        """IDでプロンプトを取得する。"""
        for p in self.prompts:
            if p.id == prompt_id:
                return p
        return None