"""プロンプトカードコンポーネント。"""

import flet as ft
from typing import Callable, Optional

from models.prompt import Prompt
from ui.styles.colors import (
    CARD_BG,
    CARD_HOVER_BG,
    BORDER_COLOR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    FAVORITE_COLOR,
    FAVORITE_INACTIVE,
)
from ui.styles.spacing import BORDER_RADIUS_MD, PADDING_MD, CARD_GAP
from ui.styles.typography import FONT_SIZE_TITLE, FONT_SIZE_BODY
from ui.styles.card_style import CARD_WIDTH, CARD_HEIGHT
from utils.text_utils import truncate_preview, truncate_title


class PromptCard(ft.Container):
    """プロンプトを表示するカードコンポーネント。"""

    def __init__(
        self,
        prompt: Prompt,
        on_click: Optional[Callable[[Prompt], None]] = None,
        on_copy: Optional[Callable[[Prompt], None]] = None,
        on_favorite: Optional[Callable[[Prompt], None]] = None,
        on_delete: Optional[Callable[[Prompt], None]] = None,
    ):
        self.prompt = prompt
        self._on_click = on_click
        self._on_copy = on_copy
        self._on_favorite = on_favorite
        self._on_delete = on_delete

        super().__init__(
            content=self._build_content(),
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            padding=PADDING_MD,
            border_radius=BORDER_RADIUS_MD,
            bgcolor=CARD_BG,
            border=ft.border.all(1, BORDER_COLOR),
            on_click=self._handle_click,
            on_hover=self._handle_hover,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )

    def _build_content(self) -> ft.Column:
        """カードの中身を構築する。"""
        # タイトル行（タイトル + お気に入りボタン）
        title_row = ft.Row(
            controls=[
                ft.Text(
                    truncate_title(self.prompt.title, 20),
                    size=FONT_SIZE_TITLE,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY,
                    expand=True,
                ),
                ft.IconButton(
                    icon=ft.Icons.STAR if self.prompt.favorite else ft.Icons.STAR_BORDER,
                    icon_color=FAVORITE_COLOR if self.prompt.favorite else FAVORITE_INACTIVE,
                    icon_size=18,
                    on_click=self._handle_favorite,
                    tooltip="お気に入り",
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        # プレビューテキスト
        preview = ft.Text(
            truncate_preview(self.prompt.body),
            size=FONT_SIZE_BODY,
            color=TEXT_SECONDARY,
            max_lines=4,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

        # アクションボタン行
        action_row = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.CONTENT_COPY,
                    icon_size=16,
                    tooltip="コピー",
                    on_click=self._handle_copy,
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_size=16,
                    tooltip="削除",
                    on_click=self._handle_delete,
                ),
            ],
            alignment=ft.MainAxisAlignment.END,
        )

        return ft.Column(
            controls=[
                title_row,
                ft.Container(content=preview, expand=True),
                action_row,
            ],
            spacing=8,
            expand=True,
        )

    def _handle_click(self, e: ft.ControlEvent) -> None:
        """カードクリック時の処理。"""
        if self._on_click:
            self._on_click(self.prompt)

    def _handle_hover(self, e: ft.ControlEvent) -> None:
        """ホバー時の処理。"""
        self.bgcolor = CARD_HOVER_BG if e.data == "true" else CARD_BG
        self.update()

    def _handle_copy(self, e: ft.ControlEvent) -> None:
        """コピーボタンクリック時の処理。"""
        page = e.control.page
        if not page:
            return
        try:
            page.set_clipboard(self.prompt.body)
            if self._on_copy:
                self._on_copy(self.prompt)
            # スナックバーで通知
            snack = ft.SnackBar(content=ft.Text("コピーしました"), duration=1500)
            page.overlay.append(snack)
            snack.open = True
            page.update()
        except Exception:
            # クリップボード操作が失敗してもアプリはクラッシュさせない
            pass

    def _handle_favorite(self, e: ft.ControlEvent) -> None:
        """お気に入りボタンクリック時の処理。"""
        if self._on_favorite:
            self._on_favorite(self.prompt)

    def _handle_delete(self, e: ft.ControlEvent) -> None:
        """削除ボタンクリック時の処理。"""
        if self._on_delete:
            self._on_delete(self.prompt)