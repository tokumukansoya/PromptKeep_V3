"""カテゴリサービス。

カテゴリの CRUD および階層移動・検証を担当。
Flet 0.28.3、Python 3.14.2 対応。

Attributes:
    MAX_CATEGORY_DEPTH: 許容されるカテゴリ階層の最大深さ。

Note:
    - 操作後はメモリ上の `AppState` を更新するのみ。
      永続化は呼び出し側（UI/アプリケーション層）で `DataService.save()` を実行する。
"""

import logging
from typing import List, Optional, Set

from config import MAX_CATEGORY_DEPTH
from models.app_state import AppState
from models.category import Category
from services.data_service import DataService
from exceptions import (
    CategoryNotFoundError,
    InvalidCategoryDepthError,
    ValidationError,
    DataPersistenceError,
)

logger = logging.getLogger(__name__)


class CategoryService:
    """カテゴリの CRUD 操作を提供するサービス。

    Attributes:
        data_service: データ永続化を担当するサービス。

    Note:
        - 本サービスは `AppState` の `categories` を直接更新する。
        - 変更の保存（JSON 書き込み）は呼び出し側の責務。
    """

    def __init__(self, data_service: DataService) -> None:
        """CategoryService の初期化。

        Args:
            data_service: DataService インスタンス。
        """
        self.data_service = data_service
        logger.debug("CategoryService initialized")

    def create_category(
        self, state: AppState, name: str, parent_id: Optional[str] = None
    ) -> Category:
        """新規カテゴリを作成する。

        兄弟末尾に追加し、`order` を自動採番する。

        Args:
            state: アプリケーション状態。
            name: カテゴリ名。
            parent_id: 親カテゴリの ID（ルートの場合は None）。

        Returns:
            生成された `Category` オブジェクト。

        Raises:
            CategoryNotFoundError: 親カテゴリが存在しない場合。
            InvalidCategoryDepthError: 深さ制約（最大階層）に違反する場合。
        """
        try:
            if parent_id is not None and state.get_category(parent_id) is None:
                logger.error("Parent category not found: %s", parent_id)
                raise CategoryNotFoundError(f"親カテゴリが見つかりません: {parent_id}")

            parent_depth = self._get_depth(state, parent_id) if parent_id else 0
            new_depth = parent_depth + 1
            if new_depth > MAX_CATEGORY_DEPTH:
                logger.error(
                    "Category depth exceeds limit on create: %s > %s",
                    new_depth,
                    MAX_CATEGORY_DEPTH,
                )
                raise InvalidCategoryDepthError(
                    f"カテゴリ階層が深すぎます（最大 {MAX_CATEGORY_DEPTH}）"
                )

            order = self._next_order_for_parent(state, parent_id)
            category = Category.create(name=name, parent_id=parent_id, order=order)
            state.categories.append(category)
            logger.info("Created category: %s (parent=%s)", category.id, parent_id)
            return category
        except (CategoryNotFoundError, InvalidCategoryDepthError):
            raise
        except Exception as exc:
            logger.exception("Failed to create category")
            raise ValidationError(f"カテゴリの作成に失敗しました: {exc}")

    def update_category(self, state: AppState, category_id: str, name: str) -> Category:
        """既存カテゴリの名称を更新する。

        Args:
            state: アプリケーション状態。
            category_id: 更新対象カテゴリの ID。
            name: 新しいカテゴリ名。

        Returns:
            更新後の `Category` オブジェクト。

        Raises:
            CategoryNotFoundError: 対象カテゴリが存在しない場合。
        """
        try:
            category = state.get_category(category_id)
            if category is None:
                logger.error("Category not found: %s", category_id)
                raise CategoryNotFoundError(f"カテゴリが見つかりません: {category_id}")

            category.name = name
            logger.info("Updated category name: %s", category_id)
            return category
        except CategoryNotFoundError:
            raise
        except Exception as exc:
            logger.exception("Failed to update category: %s", category_id)
            raise ValidationError(f"カテゴリの更新に失敗しました: {exc}")

    def delete_category(self, state: AppState, category_id: str) -> None:
        """カテゴリを削除する。

        サブツリー（配下の子孫カテゴリ）も合わせて削除する。

        Args:
            state: アプリケーション状態。
            category_id: 削除対象カテゴリの ID。

        Raises:
            CategoryNotFoundError: 対象カテゴリが存在しない場合。
        """
        try:
            target = state.get_category(category_id)
            if target is None:
                logger.error("Category not found: %s", category_id)
                raise CategoryNotFoundError(f"カテゴリが見つかりません: {category_id}")

            to_remove: Set[str] = self._get_descendant_ids(state, category_id)
            to_remove.add(category_id)

            before = len(state.categories)
            state.categories = [c for c in state.categories if c.id not in to_remove]
            after = len(state.categories)

            # 削除したカテゴリの親の兄弟順序を再採番
            self._reindex_siblings(state, target.parent_id)

            logger.info(
                "Deleted category subtree: root=%s, removed=%s",
                category_id,
                before - after,
            )
        except CategoryNotFoundError:
            raise
        except Exception as exc:
            logger.exception("Failed to delete category: %s", category_id)
            raise ValidationError(f"カテゴリの削除に失敗しました: {exc}")

    def get_category(self, state: AppState, category_id: str) -> Category:
        """ID でカテゴリを取得する。

        Args:
            state: アプリケーション状態。
            category_id: カテゴリ ID。

        Returns:
            カテゴリオブジェクト。

        Raises:
            CategoryNotFoundError: 対象カテゴリが存在しない場合。
        """
        try:
            category = state.get_category(category_id)
            if category is None:
                logger.error("Category not found: %s", category_id)
                raise CategoryNotFoundError(f"カテゴリが見つかりません: {category_id}")
            return category
        except CategoryNotFoundError:
            raise
        except Exception as exc:
            logger.exception("Failed to get category: %s", category_id)
            raise DataPersistenceError(f"カテゴリ取得に失敗しました: {exc}")

    def list_categories(self, state: AppState) -> List[Category]:
        """すべてのカテゴリを取得する。

        Args:
            state: アプリケーション状態。

        Returns:
            `Category` のリスト。
        """
        try:
            return list(state.categories)
        except Exception as exc:
            logger.exception("Failed to list categories")
            raise DataPersistenceError(f"カテゴリ取得に失敗しました: {exc}")

    def move_category(
        self, state: AppState, category_id: str, new_parent_id: Optional[str]
    ) -> Category:
        """カテゴリを別の親配下へ移動する。

        深さ制約と循環参照を検証する。サブツリーが最大深さを超える配置は拒否。

        Args:
            state: アプリケーション状態。
            category_id: 移動対象カテゴリの ID。
            new_parent_id: 新しい親カテゴリ ID（ルートへ移動する場合は None）。

        Returns:
            移動後の `Category` オブジェクト。

        Raises:
            CategoryNotFoundError: 対象カテゴリまたは親カテゴリが存在しない場合。
            InvalidCategoryDepthError: 深さ制約に違反、または循環参照となる場合。
        """
        try:
            category = state.get_category(category_id)
            if category is None:
                logger.error("Category not found: %s", category_id)
                raise CategoryNotFoundError(f"カテゴリが見つかりません: {category_id}")

            if new_parent_id is not None:
                new_parent = state.get_category(new_parent_id)
                if new_parent is None:
                    logger.error("Parent category not found: %s", new_parent_id)
                    raise CategoryNotFoundError(
                        f"親カテゴリが見つかりません: {new_parent_id}"
                    )
            else:
                new_parent = None

            # 循環参照の防止（自身または子孫を親にできない）
            descendants = self._get_descendant_ids(state, category_id)
            if new_parent_id is not None and new_parent_id in descendants.union(
                {category_id}
            ):
                logger.error(
                    "Cyclic category move detected: %s -> %s",
                    category_id,
                    new_parent_id,
                )
                raise InvalidCategoryDepthError("循環参照は許可されていません")

            # 深さ検証：新しい親の深さ + サブツリーの高さ <= MAX
            parent_depth = self._get_depth(state, new_parent_id) if new_parent else 0
            subtree_height = self._get_subtree_max_depth(state, category_id)
            if parent_depth + subtree_height > MAX_CATEGORY_DEPTH:
                logger.error(
                    "Category move exceeds depth limit: parent_depth=%s, subtree_height=%s, max=%s",
                    parent_depth,
                    subtree_height,
                    MAX_CATEGORY_DEPTH,
                )
                raise InvalidCategoryDepthError(
                    f"カテゴリ階層が深すぎます（最大 {MAX_CATEGORY_DEPTH}）"
                )

            # 親変更と order の付与（新親の末尾へ）
            old_parent_id = category.parent_id
            category.parent_id = new_parent_id
            category.order = self._next_order_for_parent(state, new_parent_id)

            # 旧親の兄弟順序を再採番
            self._reindex_siblings(state, old_parent_id)

            logger.info(
                "Moved category: %s from parent=%s to parent=%s",
                category_id,
                old_parent_id,
                new_parent_id,
            )
            return category
        except (CategoryNotFoundError, InvalidCategoryDepthError):
            raise
        except Exception as exc:
            logger.exception("Failed to move category: %s", category_id)
            raise ValidationError(f"カテゴリの移動に失敗しました: {exc}")

    def validate_depth(self, category_path: List[str]) -> bool:
        """カテゴリ階層長の単純検証を行う。

        `category_path` はルートからの名称配列を想定する（例: ["親", "子", "孫"]).

        Args:
            category_path: カテゴリ階層の配列。

        Returns:
            深さが制約内であれば True、それ以外は False。
        """
        return len(category_path) <= MAX_CATEGORY_DEPTH

    # ---------------------------------------------------------------------
    # internal helpers
    # ---------------------------------------------------------------------
    def _next_order_for_parent(self, state: AppState, parent_id: Optional[str]) -> int:
        siblings = [c for c in state.categories if c.parent_id == parent_id]
        if not siblings:
            return 0
        return max(c.order for c in siblings) + 1

    def _reindex_siblings(self, state: AppState, parent_id: Optional[str]) -> None:
        siblings = sorted(
            [c for c in state.categories if c.parent_id == parent_id],
            key=lambda c: c.order,
        )
        for i, c in enumerate(siblings):
            c.order = i

    def _get_depth(self, state: AppState, category_id: Optional[str]) -> int:
        """指定カテゴリの深さ（1 起点）を返す。

        ルート（parent_id=None）のカテゴリは深さ 1。
        `category_id` が None の場合は 0（ルート階層の外）を返す。
        """
        if category_id is None:
            return 0
        depth = 0
        current = state.get_category(category_id)
        while current is not None:
            depth += 1
            if current.parent_id is None:
                break
            current = state.get_category(current.parent_id)
        return depth

    def _get_descendant_ids(self, state: AppState, category_id: str) -> Set[str]:
        children_map = {}
        for c in state.categories:
            children_map.setdefault(c.parent_id, []).append(c)

        result: Set[str] = set()
        stack: List[str] = [category_id]
        while stack:
            cid = stack.pop()
            for child in children_map.get(cid, []):
                result.add(child.id)
                stack.append(child.id)
        return result

    def _get_subtree_max_depth(self, state: AppState, root_id: str) -> int:
        """サブツリーの最大深さ（根を 1 とする）を求める。"""
        children_map = {}
        for c in state.categories:
            children_map.setdefault(c.parent_id, []).append(c)

        max_depth = 1

        def dfs(cid: str, depth: int) -> None:
            nonlocal max_depth
            max_depth = max(max_depth, depth)
            for child in children_map.get(cid, []):
                dfs(child.id, depth + 1)

        dfs(root_id, 1)
        return max_depth
