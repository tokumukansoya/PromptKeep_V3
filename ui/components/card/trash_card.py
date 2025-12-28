"""ゴミ箱用プロンプトカードコンポーネント。"""

import flet as ft
from typing import Callable, Optional

from models.prompt import Prompt
from ui.styles.colors import (
    CARD_BG,
    CARD_HOVER_BG,
    BORDER_COLOR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ERROR_COLOR,
    SUCCESS_COLOR,
)
from ui.styles.spacing import BORDER_RADIUS_MD, PADDING_MD
from ui.styles.typography import FONT_SIZE_TITLE, FONT_SIZE_BODY
from ui.styles.card_style import CARD_WIDTH, CARD_HEIGHT
from utils.text_utils import truncate_preview, truncate_title


class TrashCard(ft.Container):
    """ゴミ箱内のプロンプトを表示するカードコンポーネント。"""

    def __init__(
        self,
        prompt: Prompt,
        on_restore: Optional[Callable[[Prompt], None]] = None,
        on_permanent_delete: Optional[Callable[[Prompt], None]] = None,
    ):
        self.prompt = prompt
        self._on_restore = on_restore
        self._on_permanent_delete = on_permanent_delete

        super().__init__(
            content=self._build_content(),
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            padding=PADDING_MD,
            border_radius=BORDER_RADIUS_MD,
            bgcolor=CARD_BG,
            border=ft.border.all(1, BORDER_COLOR),
            on_hover=self._handle_hover,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )

    def _build_content(self) -> ft.Column:
        """カードの中身を構築する。"""
        # タイトル
        title_text = ft.Text(
            truncate_title(self.prompt.title, 25),
            size=FONT_SIZE_TITLE,
            weight=ft.FontWeight.BOLD,
            color=TEXT_PRIMARY,
        )

        # プレビューテキスト
        preview = ft.Text(
            truncate_preview(self.prompt.body),
            size=FONT_SIZE_BODY,
            color=TEXT_SECONDARY,
            max_lines=3,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

        # 削除日時
        deleted_info = ft.Text(
            f"削除日: {self.prompt.deleted_at.strftime('%Y/%m/%d %H:%M') if self.prompt.deleted_at else '不明'}",
            size=10,
            color=TEXT_SECONDARY,
        )

        # アクションボタン行
        action_row = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.RESTORE,
                    icon_color=SUCCESS_COLOR,
                    icon_size=20,
                    tooltip="復元",
                    on_click=self._handle_restore,
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_FOREVER,
                    icon_color=ERROR_COLOR,
                    icon_size=20,
                    tooltip="完全に削除",
                    on_click=self._handle_permanent_delete,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=16,
        )

        return ft.Column(
            controls=[
                title_text,
                ft.Container(content=preview, expand=True),
                deleted_info,
                action_row,
            ],
            spacing=8,
            expand=True,
        )

    def _handle_hover(self, e: ft.ControlEvent) -> None:
        """ホバー時の処理。"""
        self.bgcolor = CARD_HOVER_BG if e.data == "true" else CARD_BG
        self.update()

    def _handle_restore(self, e: ft.ControlEvent) -> None:
        """復元ボタンクリック時の処理。"""
        if self._on_restore:
            self._on_restore(self.prompt)

    def _handle_permanent_delete(self, e: ft.ControlEvent) -> None:
        """完全削除ボタンクリック時の処理。"""
        if self._on_permanent_delete:
            self._on_permanent_delete(self.prompt)
