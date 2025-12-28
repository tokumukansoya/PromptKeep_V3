"""カテゴリサービス。"""

from typing import List, Optional

from models.category import Category


class CategoryService:
    """カテゴリのCRUD操作を提供するサービス。"""

    def create_category(self, name: str, order: int = 0) -> Category:
        """新しいカテゴリを作成する。"""
        return Category.create(name=name, order=order)

    def update_category(
        self,
        category: Category,
        name: Optional[str] = None,
        order: Optional[int] = None,
    ) -> Category:
        """カテゴリを更新する。"""
        if name is not None:
            category.name = name
        if order is not None:
            category.order = order
        return category

    def get_sorted_categories(self, categories: List[Category]) -> List[Category]:
        """カテゴリをorder順にソートする。"""
        return sorted(categories, key=lambda c: c.order)

    def reorder_categories(self, categories: List[Category]) -> List[Category]:
        """カテゴリの順序を再割り当てする。"""
        for i, category in enumerate(categories):
            category.order = i
        return categories