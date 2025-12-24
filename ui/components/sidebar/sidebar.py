from __future__ import annotations

from typing import Callable, List

import flet as ft

from models.category import Category
from ui.components.sidebar.search_box import SearchBox
from ui.components.sidebar.category_tree import CategoryTree
from ui.components.sidebar.add_category_button import AddCategoryButton
from ui.styles import colors, spacing


class Sidebar(ft.Column):
    """サイドバー全体コンポーネント。

    上部に検索、中央にカテゴリツリー、下部にカテゴリ追加ボタンを
    垂直に配置します。イベントはコールバックで呼び出し側へ通知します。

    Args:
        categories: 表示する全カテゴリ一覧。
        on_search: 検索クエリ変更時のコールバック。文字列を渡す。
        on_category_select: カテゴリ選択時のコールバック。選択 `Category` を渡す。
        on_category_add: カテゴリ追加ボタンクリック時のコールバック。
        on_category_move: DnD によるカテゴリ移動時のコールバック。`(source_id, target_parent_id)` を渡す。
    """

    def __init__(
        self,
        categories: List[Category],
        on_search: Callable[[str], None],
        on_category_select: Callable[[Category], None],
        on_category_add: Callable[[], None],
        on_category_move: Callable[[str, str], None],
    ) -> None:
        """初期化。"""
        super().__init__()

        self._categories: List[Category] = categories
        self._on_search: Callable[[str], None] = on_search
        self._on_category_select: Callable[[Category], None] = on_category_select
        self._on_category_add: Callable[[], None] = on_category_add
        self._on_category_move: Callable[[str, str], None] = on_category_move

        # 上部：検索ボックス（デバウンスは SearchBox 内で実施）
        search_box = SearchBox(on_search=self._on_search)

        # 中央：カテゴリツリー
        category_tree = CategoryTree(
            categories=self._categories,
            on_select=self._on_category_select,
            on_move=self._on_category_move,
        )

        # 下部：カテゴリ追加ボタン
        add_button = AddCategoryButton(on_click=self._on_category_add)

        # レイアウト構成
        self.controls = [
            ft.Container(
                content=search_box, padding=ft.padding.only(bottom=spacing.GAP_MD)
            ),
            ft.Container(content=category_tree, expand=True),
            ft.Container(
                content=add_button, padding=ft.padding.only(top=spacing.GAP_MD)
            ),
        ]
        self.spacing = spacing.GAP_MD
        self.tight = True

    def build(self) -> ft.Column:  # type: ignore[override]
        """Flet ビルド関数。

        Returns:
            Column: 自身のインスタンスを返します。
        """
        return self
