"""カテゴリモデル。"""

from dataclasses import dataclass
import uuid


@dataclass
class Category:
    """カテゴリを表すデータクラス。"""

    id: str
    name: str
    order: int = 0

    @classmethod
    def create(cls, name: str, order: int = 0) -> "Category":
        """新しいカテゴリを作成する。"""
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            order=order,
        )

    def to_dict(self) -> dict:
        """辞書に変換する。"""
        return {
            "id": self.id,
            "name": self.name,
            "order": self.order,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        """辞書からカテゴリを作成する。
        
        Args:
            data: カテゴリデータの辞書
            
        Returns:
            Category インスタンス
        """
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", "(名前なし)"),
            order=data.get("order", 0),
        )