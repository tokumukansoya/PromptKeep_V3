from __future__ import annotations

from typing import Callable

import flet as ft

from config import MAX_CATEGORY_DEPTH
from models.category import Category
from ui.styles import colors, spacing


class CategoryItem(ft.Draggable):
    """カテゴリ一覧に表示するドラッグ可能なアイテム。

    自身を `ft.Draggable` として提供し、内部に `ft.DragTarget` を配置して
    ドロップ受け入れも可能にします。クリックで選択、ドロップで移動を
    呼び出し側へ通知します。

    Args:
        category: 表示対象のカテゴリ。
        on_click: カテゴリ選択時に呼ばれるコールバック。引数に `Category` を渡す。
        on_drag: ドロップ受け入れ時に呼ばれるコールバック。引数は `(source_id, target_parent_id)`。
    """

    def __init__(
        self,
        category: Category,
        on_click: Callable[[Category], None],
        on_drag: Callable[[str, str], None],
    ) -> None:
        """初期化。

        Args:
            category: 表示対象のカテゴリ。
            on_click: カテゴリ選択時のコールバック。
            on_drag: ドロップ受け入れ時のコールバック。
        """
        # 簡易インデント計算：親がある場合は 1 レベル。より深い階層は
        # リスト構築側で必要に応じて調整してください。
        level = 0 if category.parent_id is None else 1
        level = max(0, min(level, MAX_CATEGORY_DEPTH - 1))
        indent_px = level * spacing.PADDING_MD

        # 表示行（クリック対応）
        row = ft.Row(
            controls=[
                ft.Icon(
                    name="folder_rounded",
                    color=colors.TEXT_PRIMARY,
                    size=spacing.ICON_SIZE,
                ),
                ft.Text(value=category.name, color=colors.TEXT_PRIMARY),
            ],
            spacing=spacing.GAP_XS,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        clickable = ft.GestureDetector(content=row, on_tap=lambda _: on_click(category))

        # ドロップ受け入れターゲット（このアイテム配下へ移動）
        target = ft.DragTarget(
            content=ft.Container(
                content=clickable, padding=ft.padding.only(left=indent_px)
            ),
            on_accept=lambda e: self._handle_accept(e, on_drag),
        )

        # Draggable 本体の初期化（このカテゴリ自身をドラッグ可能にする）
        super().__init__(
            group="category",
            content=target,
            data=category.id,
        )
        self._category = category
        self._on_click = on_click
        self._on_drag = on_drag

    def _handle_accept(
        self, e: ft.DragTargetAcceptEvent, on_drag: Callable[[str, str], None]
    ) -> None:
        """ドロップ受け入れイベント。移動処理をコールバックへ通知する。

        Args:
            e: ドロップイベント。`e.data` にドラッグ元のカテゴリ ID が入る。
            on_drag: コールバック。`(source_id, target_parent_id)` を渡す。
        """
        source_id = e.data
        target_parent_id = self._category.id
        on_drag(source_id, target_parent_id)

    def build(self) -> ft.Draggable:  # type: ignore[override]
        """Flet ビルド関数。

        Returns:
            Draggable: 自身のインスタンスを返します。
        """
        return self
