"""サイドバーコンポーネント。

ナビゲーション用のサイドバーを提供する。
カテゴリ選択、お気に入り、ゴミ箱へのナビゲーションを含む。
"""

import flet as ft
from typing import Callable, Optional, List, Dict

from models.category import Category
from ui.styles.colors import (
    SIDEBAR_BG,
    SIDEBAR_ITEM_HOVER,
    SIDEBAR_ITEM_SELECTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ACCENT_PRIMARY,
)
from ui.styles.spacing import SIDEBAR_WIDTH, PADDING_MD, PADDING_SM, SIDEBAR_ITEM_HEIGHT
from ui.styles.typography import FONT_SIZE_BODY, FONT_SIZE_SM


class SidebarItem(ft.Container):
    """サイドバーの単一項目。

    Attributes:
        _selected: 選択状態
    """

    def __init__(
        self,
        icon: str,
        text: str,
        selected: bool = False,
        on_click: Optional[Callable[[], None]] = None,
        badge_count: int = 0,
    ) -> None:
        """初期化。

        Args:
            icon: アイコン名
            text: 表示テキスト
            selected: 選択状態
            on_click: クリック時のコールバック
            badge_count: バッジに表示する数値
        """
        self._selected = selected
        self._on_click_callback = on_click

        # バッジ（カウント表示）
        badge = None
        if badge_count > 0:
            badge = ft.Container(
                content=ft.Text(str(badge_count), size=FONT_SIZE_SM, color=TEXT_PRIMARY),
                bgcolor=ACCENT_PRIMARY,
                border_radius=10,
                padding=ft.padding.symmetric(horizontal=6, vertical=2),
            )

        super().__init__(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, size=20, color=TEXT_PRIMARY if selected else TEXT_SECONDARY),
                    ft.Text(
                        text,
                        size=FONT_SIZE_BODY,
                        color=TEXT_PRIMARY if selected else TEXT_SECONDARY,
                        expand=True,
                    ),
                    badge if badge else ft.Container(),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=PADDING_MD, vertical=PADDING_SM),
            height=SIDEBAR_ITEM_HEIGHT,
            border_radius=8,
            bgcolor=SIDEBAR_ITEM_SELECTED if selected else None,
            on_click=self._handle_click,
            on_hover=self._handle_hover,
        )

    def _handle_click(self, e: ft.ControlEvent) -> None:
        """クリックイベントを処理する。"""
        if self._on_click_callback:
            self._on_click_callback()

    def _handle_hover(self, e: ft.ControlEvent) -> None:
        """ホバーイベントを処理する。"""
        if not self._selected:
            is_hovered = e.data == "true"
            self.bgcolor = SIDEBAR_ITEM_HOVER if is_hovered else None
            self.update()


class Sidebar(ft.Container):
    """サイドバー全体のコンポーネント。

    カテゴリ一覧、お気に入り、ゴミ箱へのナビゲーションを提供する。

    Attributes:
        categories: カテゴリのリスト
        view_mode: 現在のビューモード
    """

    def __init__(
        self,
        categories: List[Category],
        selected_category_id: Optional[str],
        prompt_counts: Dict[str, int],
        on_category_select: Optional[Callable[[Optional[str]], None]] = None,
        on_add_category: Optional[Callable[[], None]] = None,
        on_delete_category: Optional[Callable[[Category], None]] = None,
        on_show_all: Optional[Callable[[], None]] = None,
        on_show_favorites: Optional[Callable[[], None]] = None,
        on_show_trash: Optional[Callable[[], None]] = None,
        view_mode: str = "all",  # "all", "favorites", "trash", "category"
    ):
        self.categories = categories
        self.selected_category_id = selected_category_id
        self.prompt_counts = prompt_counts
        self._on_category_select = on_category_select
        self._on_add_category = on_add_category
        self._on_delete_category = on_delete_category
        self._on_show_all = on_show_all
        self._on_show_favorites = on_show_favorites
        self._on_show_trash = on_show_trash
        self.view_mode = view_mode

        super().__init__(
            content=self._build_content(),
            width=SIDEBAR_WIDTH,
            bgcolor=SIDEBAR_BG,
            padding=PADDING_MD,
        )

    def _build_content(self) -> ft.Column:
        """サイドバーの中身を構築する。"""
        items = []

        # ヘッダー
        header = ft.Container(
            content=ft.Text(
                "PromptKeep",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=TEXT_PRIMARY,
            ),
            padding=ft.padding.only(bottom=PADDING_MD),
        )
        items.append(header)

        # すべてのプロンプト
        items.append(
            SidebarItem(
                icon=ft.Icons.HOME,
                text="すべて",
                selected=self.view_mode == "all",
                on_click=self._on_show_all,
                badge_count=self.prompt_counts.get("all", 0),
            )
        )

        # お気に入り
        items.append(
            SidebarItem(
                icon=ft.Icons.STAR,
                text="お気に入り",
                selected=self.view_mode == "favorites",
                on_click=self._on_show_favorites,
                badge_count=self.prompt_counts.get("favorites", 0),
            )
        )

        # 区切り線
        items.append(ft.Divider(height=20, color="#3A3A3A"))

        # カテゴリヘッダー
        category_header = ft.Row(
            controls=[
                ft.Text("カテゴリ", size=FONT_SIZE_SM, color=TEXT_SECONDARY),
                ft.IconButton(
                    icon=ft.Icons.ADD,
                    icon_size=16,
                    tooltip="カテゴリを追加",
                    on_click=lambda _: self._on_add_category() if self._on_add_category else None,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        items.append(category_header)

        # カテゴリ一覧
        for category in self.categories:
            is_selected = (
                self.view_mode == "category" and self.selected_category_id == category.id
            )
            category_item = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.FOLDER, size=20, color=TEXT_PRIMARY if is_selected else TEXT_SECONDARY),
                        ft.Text(
                            category.name,
                            size=FONT_SIZE_BODY,
                            color=TEXT_PRIMARY if is_selected else TEXT_SECONDARY,
                            expand=True,
                        ),
                        ft.Text(
                            str(self.prompt_counts.get(category.id, 0)),
                            size=FONT_SIZE_SM,
                            color=TEXT_SECONDARY,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_size=14,
                            tooltip="カテゴリを削除",
                            on_click=lambda e, c=category: self._handle_delete_category(c),
                        ),
                    ],
                    spacing=8,
                ),
                padding=ft.padding.symmetric(horizontal=PADDING_MD, vertical=PADDING_SM),
                height=SIDEBAR_ITEM_HEIGHT,
                border_radius=8,
                bgcolor=SIDEBAR_ITEM_SELECTED if is_selected else None,
                on_click=lambda e, c=category: self._handle_category_click(c),
            )
            items.append(category_item)

        # 区切り線
        items.append(ft.Divider(height=20, color="#3A3A3A"))

        # ゴミ箱
        items.append(
            SidebarItem(
                icon=ft.Icons.DELETE,
                text="ゴミ箱",
                selected=self.view_mode == "trash",
                on_click=self._on_show_trash,
                badge_count=self.prompt_counts.get("trash", 0),
            )
        )

        return ft.Column(
            controls=items,
            spacing=4,
            expand=True,
        )

    def _handle_category_click(self, category: Category) -> None:
        if self._on_category_select:
            self._on_category_select(category.id)

    def _handle_delete_category(self, category: Category) -> None:
        if self._on_delete_category:
            self._on_delete_category(category)
