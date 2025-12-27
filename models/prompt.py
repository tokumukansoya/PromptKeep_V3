"""Prompt データモデル。

プロンプト情報を表現するデータクラス。
Flet 0.28.3、Python 3.14.2 対応。
"""

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Prompt:
    """プロンプトデータモデル。

    プロンプトの単位となるデータクラス。
    タイトル、本文、カテゴリ階層、お気に入り状態を管理。

    Attributes:
        id: プロンプトの一意識別子（UUID）。
        title: プロンプトのタイトル。
        body: プロンプトの本文。
        category_ids: カテゴリIDの階層 ["cat1_id", "cat2_id", "cat3_id"]。未分類は []。
        favorite: お気に入り状態。
        deleted_at: 削除時刻（削除されていない場合は None）。
        created_at: 作成時刻。
        updated_at: 更新時刻。

    Note:
        - id は自動生成（uuid4）。
        - category_ids は最大 3 階層（config.MAX_CATEGORY_DEPTH 参照）。
        - カテゴリ名変更時もプロンプトは影響を受けない（IDベース）。
        - deleted_at が None でない場合、プロンプトは論理削除状態。
    """

    id: str
    title: str
    body: str
    category_ids: List[str]  # カテゴリIDの配列（名前ではなくID）
    favorite: bool
    deleted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(title: str, body: str, category_ids: Optional[List[str]] = None) -> "Prompt":
        """新規プロンプトを作成する。

        Args:
            title: プロンプトのタイトル。
            body: プロンプトの本文。
            category_ids: カテゴリID階層（未指定時は []）。

        Returns:
            新規作成された Prompt オブジェクト。

        Example:
            >>> prompt = Prompt.create("タイトル", "本文")
            >>> print(prompt.id)
            3fa85f64-5717-4562-b3fc-2c963f66afa6
        """
        if category_ids is None:
            category_ids = []

        now = datetime.now()
        return Prompt(
            id=str(uuid.uuid4()),
            title=title,
            body=body,
            category_ids=category_ids,
            favorite=False,
            deleted_at=None,
            created_at=now,
            updated_at=now,
        )

    def to_dict(self) -> dict:
        """Prompt オブジェクトを辞書に変換。

        JSON 保存用の辞書形式に変換。

        Returns:
            辞書形式の Prompt データ。

        Example:
            >>> prompt = Prompt.create("title", "body")
            >>> d = prompt.to_dict()
            >>> print(d["title"])
            title
        """
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

    @staticmethod
    def from_dict(data: dict) -> "Prompt":
        """辞書から Prompt オブジェクトを構築。

        JSON から読み込んだ辞書を Prompt に変換。

        Args:
            data: Prompt データの辞書。

        Returns:
            構築された Prompt オブジェクト。

        Raises:
            ValueError: 必須フィールドが不足している場合。
            TypeError: フィールドの型が不正な場合。

        Example:
            >>> data = {
            ...     "id": "uuid",
            ...     "title": "title",
            ...     "body": "body",
            ...     "category_ids": [],
            ...     "favorite": False,
            ...     "deleted_at": None,
            ...     "created_at": "2025-01-01T00:00:00",
            ...     "updated_at": "2025-01-01T00:00:00"
            ... }
            >>> prompt = Prompt.from_dict(data)
        """
        try:
            return Prompt(
                id=data["id"],
                title=data["title"],
                body=data["body"],
                category_ids=data.get("category_ids", []),
                favorite=data.get("favorite", False),
                deleted_at=(
                    datetime.fromisoformat(data["deleted_at"]) if data.get("deleted_at") else None
                ),
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"]),
            )
        except KeyError as e:
            raise ValueError(f"必須フィールドが不足しています: {e}")
        except (TypeError, ValueError) as e:
            raise TypeError(f"フィールドの型が不正です: {e}")
