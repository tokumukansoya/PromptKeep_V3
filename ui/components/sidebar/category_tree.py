from __future__ import annotations

from typing import Callable, List, Dict, Optional, Set

import flet as ft

from models.category import Category
from ui.components.sidebar.category_item import CategoryItem
from ui.styles import spacing


class CategoryTree(ft.Column):
    """カテゴリツリー表示コンポーネント。

    平坦なカテゴリリストから階層構造を生成し、`CategoryItem` を再帰的に
    配置します。子を持つカテゴリには展開／折りたたみのトグルを表示します。

    Args:
        categories: すべてのカテゴリ（親子関係は `parent_id` で表現）。
        on_select: カテゴリ選択時のコールバック。選択された `Category` を渡す。
        on_move: DnD による移動時のコールバック。`(source_id, target_parent_id)` を渡す。
    """

    def __init__(
        self,
        categories: List[Category],
        on_select: Callable[[Category], None],
        on_move: Callable[[str, str], None],
    ) -> None:
        """初期化。"""
        super().__init__()
        self._categories: List[Category] = categories
        self._on_select: Callable[[Category], None] = on_select
        self._on_move: Callable[[str, str], None] = on_move
        self._expanded_ids: Set[str] = (
            set()
        )  # 展開状態のカテゴリ ID（子があるものを既定で展開）

        self.spacing = spacing.GAP_XS
        self.tight = True

        self._rebuild()

    # ------------------------------------------------------------------
    # internal build helpers
    # ------------------------------------------------------------------
    def _build_children_map(self) -> Dict[Optional[str], List[Category]]:
        children: Dict[Optional[str], List[Category]] = {}
        for c in self._categories:
            children.setdefault(c.parent_id, []).append(c)
        # order, name の順で安定ソート
        for pid in children:
            children[pid].sort(key=lambda x: (x.order, x.name))
        return children

    def _ensure_initial_expanded(
        self, children_map: Dict[Optional[str], List[Category]]
    ) -> None:
        # 子を持つカテゴリは既定で展開状態に
        for cat in self._categories:
            if children_map.get(cat.id):
                self._expanded_ids.add(cat.id)

    def _rebuild(self) -> None:
        children_map = self._build_children_map()
        if not self._expanded_ids:
            self._ensure_initial_expanded(children_map)

        controls: List[ft.Control] = []
        for root in children_map.get(None, []):
            controls.extend(self._build_subtree(root, children_map, depth=0))

        self.controls = controls

    def _build_subtree(
        self,
        node: Category,
        children_map: Dict[Optional[str], List[Category]],
        depth: int,
    ) -> List[ft.Control]:
        has_children = bool(children_map.get(node.id))
        expanded = node.id in self._expanded_ids

        # トグル（子がある場合のみ表示）
        toggle_btn: ft.Control
        if has_children:
            icon = (
                ft.icons.KEYBOARD_ARROW_DOWN
                if expanded
                else ft.icons.KEYBOARD_ARROW_RIGHT
            )
            toggle_btn = ft.IconButton(
                icon=icon,
                tooltip="展開/折りたたみ",
                on_click=lambda _: self._toggle(node.id),
                icon_size=spacing.ICON_SIZE,
            )
        else:
            # アイコンサイズ相当のプレースホルダで整列
            toggle_btn = ft.Container(width=spacing.ICON_SIZE, height=spacing.ICON_SIZE)

        # アイテム本体（クリック・DnD 対応）
        item = CategoryItem(
            category=node,
            on_click=self._on_select,
            on_drag=self._on_move,
        )

        row = ft.Row(
            controls=[toggle_btn, item],
            spacing=spacing.GAP_XS,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # CategoryItem 自身が 0/1 レベルのインデントを持つため、深さに応じて追加のインデントを付加
        # 深さ 0 の場合は 0、深さ 1 以上は (depth-1) * PADDING_MD
        extra_indent = max(depth - 1, 0) * spacing.PADDING_MD
        wrapped = ft.Container(content=row, padding=ft.padding.only(left=extra_indent))

        built: List[ft.Control] = [wrapped]
        if has_children and expanded:
            for child in children_map.get(node.id, []):
                built.extend(self._build_subtree(child, children_map, depth=depth + 1))
        return built

    def _toggle(self, category_id: str) -> None:
        if category_id in self._expanded_ids:
            self._expanded_ids.remove(category_id)
        else:
            self._expanded_ids.add(category_id)
        self._rebuild()
        if self.page:
            self.page.update()

    def build(self) -> ft.Column:  # type: ignore[override]
        """Flet ビルド関数。

        Returns:
            Column: 自身のインスタンスを返します。
        """
        return self
