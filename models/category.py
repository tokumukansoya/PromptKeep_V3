"""Category データモデル。

カテゴリ情報を表現するデータクラス。
Flet 0.28.3、Python 3.14.2 対応。
"""

import uuid
from dataclasses import dataclass


@dataclass
class Category:
    """カテゴリデータモデル。

    カテゴリはフラットな一覧で管理されます（親子関係はサポートしません）。

    Attributes:
        id: カテゴリの一意識別子（UUID）。
        name: カテゴリ名。
        order: 表示順序（必要に応じて使用）。

    Note:
        - id は自動生成（uuid4）。
        - 階層はサポートしない（parent_id は廃止）。
    """

    id: str
    name: str
    order: int

    @staticmethod
    def create(name: str, order: int = 0) -> "Category":
        """新規カテゴリを作成する。

        Args:
            name: カテゴリ名。
            order: 表示順序。

        Returns:
            新規作成された Category オブジェクト。

        Example:
            >>> category = Category.create("AI")
            >>> print(category.name)
            AI
        """
        return Category(id=str(uuid.uuid4()), name=name, order=order)

    def to_dict(self) -> dict:
        """Category オブジェクトを辞書に変換（JSON 保存用）。"""
        return {
            "id": self.id,
            "name": self.name,
            "order": self.order,
        }

    @staticmethod
    def from_dict(data: dict) -> "Category":
        """辞書から Category オブジェクトを構築。

        互換性のため、旧データに `parent_id` が含まれていても無視します。
        """
        try:
            return Category(
                id=data["id"],
                name=data["name"],
                order=data.get("order", 0),
            )
        except KeyError as e:
            raise ValueError(f"必須フィールドが不足しています: {e}") from e
        except (TypeError, ValueError) as e:
            raise TypeError(f"フィールドの型が不正です: {e}") from e
