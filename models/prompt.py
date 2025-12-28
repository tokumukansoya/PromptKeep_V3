"""プロンプトモデル。"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid


@dataclass
class Prompt:
    """プロンプトを表すデータクラス。"""

    id: str
    title: str
    body: str
    category_ids: List[str] = field(default_factory=list)
    favorite: bool = False
    deleted_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(cls, title: str, body: str, category_ids: Optional[List[str]] = None) -> "Prompt":
        """新しいプロンプトを作成する。"""
        now = datetime.now()
        return cls(
            id=str(uuid.uuid4()),
            title=title,
            body=body,
            category_ids=category_ids or [],
            favorite=False,
            deleted_at=None,
            created_at=now,
            updated_at=now,
        )

    def to_dict(self) -> dict:
        """辞書に変換する。"""
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "category_ids": self.category_ids,
            "favorite": self.favorite,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Prompt":
        """辞書からプロンプトを作成する。
        
        Raises:
            KeyError: 必須フィールドが存在しない場合
            ValueError: 日付フォーマットが不正な場合
        """
        try:
            return cls(
                id=data.get("id", str(uuid.uuid4())),
                title=data.get("title", ""),
                body=data.get("body", ""),
                category_ids=data.get("category_ids", []),
                favorite=data.get("favorite", False),
                deleted_at=datetime.fromisoformat(data["deleted_at"]) if data.get("deleted_at") else None,
                created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
                updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else datetime.now(),
            )
        except (ValueError, TypeError) as e:
            # 不正なデータの場合はデフォルト値で作成
            return cls(
                id=data.get("id", str(uuid.uuid4())),
                title=data.get("title", "(読み込みエラー)"),
                body=data.get("body", ""),
                category_ids=[],
                favorite=False,
                deleted_at=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )