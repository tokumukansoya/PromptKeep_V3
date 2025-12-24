"""Category データモデル。

カテゴリ情報を表現するデータクラス。
Flet 0.28.3、Python 3.14.2 対応。
"""

from dataclasses import dataclass
from typing import Optional
import uuid


@dataclass
class Category:
    """カテゴリデータモデル。

    カテゴリの単位となるデータクラス。
    階層構造（親子関係）をサポート。

    Attributes:
        id: カテゴリの一意識別子（UUID）。
        name: カテゴリ名。
        parent_id: 親カテゴリの ID（ルートの場合は None）。
        order: 同じ親内での表示順序。

    Note:
        - id は自動生成（uuid4）。
        - 最大階層深さは config.MAX_CATEGORY_DEPTH で定義。
        - order は D&D で並べ替え時に更新。
    """

    id: str
    name: str
    parent_id: Optional[str]
    order: int

    @staticmethod
    def create(
        name: str, parent_id: Optional[str] = None, order: int = 0
    ) -> "Category":
        """新規カテゴリを作成する。

        Args:
            name: カテゴリ名。
            parent_id: 親カテゴリの ID（ルートの場合は None）。
            order: 表示順序。

        Returns:
            新規作成された Category オブジェクト。

        Example:
            >>> category = Category.create("AI")
            >>> print(category.name)
            AI
        """
        return Category(
            id=str(uuid.uuid4()), name=name, parent_id=parent_id, order=order
        )

    def to_dict(self) -> dict:
        """Category オブジェクトを辞書に変換。

        JSON 保存用の辞書形式に変換。

        Returns:
            辞書形式の Category データ。

        Example:
            >>> category = Category.create("AI")
            >>> d = category.to_dict()
            >>> print(d["name"])
            AI
        """
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
            "order": self.order,
        }

    @staticmethod
    def from_dict(data: dict) -> "Category":
        """辞書から Category オブジェクトを構築。

        JSON から読み込んだ辞書を Category に変換。

        Args:
            data: Category データの辞書。

        Returns:
            構築された Category オブジェクト。

        Raises:
            ValueError: 必須フィールドが不足している場合。
            TypeError: フィールドの型が不正な場合。

        Example:
            >>> data = {
            ...     "id": "uuid",
            ...     "name": "AI",
            ...     "parent_id": None,
            ...     "order": 0
            ... }
            >>> category = Category.from_dict(data)
        """
        try:
            return Category(
                id=data["id"],
                name=data["name"],
                parent_id=data.get("parent_id"),
                order=data.get("order", 0),
            )
        except KeyError as e:
            raise ValueError(f"必須フィールドが不足しています: {e}")
        except (TypeError, ValueError) as e:
            raise TypeError(f"フィールドの型が不正です: {e}")
