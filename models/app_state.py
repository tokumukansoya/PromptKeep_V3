"""AppState - アプリケーション状態管理。

アプリケーション全体の状態を一元管理するクラス。
Flet 0.28.3、Python 3.14.2 対応。
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from models.prompt import Prompt
from models.category import Category


@dataclass
class AppState:
    """アプリケーション全体の状態。

    プロンプト、カテゴリ、ゴミ箱、UI 状態をまとめて管理。

    Attributes:
        prompts: すべてのプロンプト（削除済みを含む）。
        categories: すべてのカテゴリ。
        trash: 削除済みプロンプト ID のリスト。
        selected_category_id: 選択中のカテゴリ ID（None = 全表示）。
        search_query: 検索クエリ。
        current_editing_id: 編集中のプロンプト ID（None = 編集なし）。
        undo_stack: アンドゥ用のスタック（直前の状態を保持）。

    Note:
        - 状態は イミュータブル に更新（新しい AppState を作成）。
        - 変更後は自動保存（サービス層で処理）。
    """

    prompts: List[Prompt] = field(default_factory=list)
    categories: List[Category] = field(default_factory=list)
    trash: List[str] = field(default_factory=list)  # prompt IDs
    selected_category_id: Optional[str] = None
    search_query: str = ""
    current_editing_id: Optional[str] = None
    undo_stack: List[dict] = field(default_factory=list)

    @staticmethod
    def empty() -> "AppState":
        """空の AppState を作成。

        Returns:
            初期化された AppState オブジェクト。

        Example:
            >>> state = AppState.empty()
            >>> print(len(state.prompts))
            0
        """
        return AppState()

    def to_dict(self) -> dict:
        """AppState を辞書に変換。

        JSON 保存用の形式に変換。

        Returns:
            辞書形式の AppState データ。
        """
        return {
            "prompts": [p.to_dict() for p in self.prompts],
            "categories": [c.to_dict() for c in self.categories],
            "trash": self.trash,
            "metadata": {
                "selected_category_id": self.selected_category_id,
                "search_query": self.search_query,
                "current_editing_id": self.current_editing_id,
            },
        }

    @staticmethod
    def from_dict(data: dict) -> "AppState":
        """辞書から AppState を構築。

        JSON から読み込んだ辞書を AppState に変換。

        Args:
            data: AppState データの辞書。

        Returns:
            構築された AppState オブジェクト。

        Raises:
            ValueError: データ形式が不正な場合。
            TypeError: フィールド型が不正な場合。

        Example:
            >>> data = {
            ...     "prompts": [],
            ...     "categories": [],
            ...     "trash": [],
            ...     "metadata": {}
            ... }
            >>> state = AppState.from_dict(data)
        """
        try:
            prompts = [Prompt.from_dict(p) for p in data.get("prompts", [])]
            categories = [Category.from_dict(c) for c in data.get("categories", [])]
            trash = data.get("trash", [])
            metadata = data.get("metadata", {})

            return AppState(
                prompts=prompts,
                categories=categories,
                trash=trash,
                selected_category_id=metadata.get("selected_category_id"),
                search_query=metadata.get("search_query", ""),
                current_editing_id=metadata.get("current_editing_id"),
            )
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"AppState の構築に失敗しました: {e}")

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """ID でプロンプトを取得。

        Args:
            prompt_id: プロンプト ID。

        Returns:
            プロンプトオブジェクト、見つからない場合は None。
        """
        return next((p for p in self.prompts if p.id == prompt_id), None)

    def get_category(self, category_id: str) -> Optional[Category]:
        """ID でカテゴリを取得。

        Args:
            category_id: カテゴリ ID。

        Returns:
            カテゴリオブジェクト、見つからない場合は None。
        """
        return next((c for c in self.categories if c.id == category_id), None)

    def get_active_prompts(self) -> List[Prompt]:
        """削除されていないプロンプトを取得。

        Returns:
            アクティブなプロンプトリスト。
        """
        return [p for p in self.prompts if p.deleted_at is None]

    def get_deleted_prompts(self) -> List[Prompt]:
        """削除されたプロンプトを取得（ゴミ箱用）。

        Returns:
            削除済みプロンプトリスト。
        """
        return [p for p in self.prompts if p.deleted_at is not None]
