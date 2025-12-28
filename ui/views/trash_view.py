"""ゴミ箱ビュー。"""

import flet as ft
from typing import Callable, List, Optional

from models.prompt import Prompt
from ui.components.card.trash_card import TrashCard
from ui.styles.spacing import CARD_GAP, PADDING_MD
from ui.styles.colors import TEXT_PRIMARY, TEXT_SECONDARY, ERROR_COLOR


class TrashView(ft.Container):
    """ゴミ箱内のプロンプトを表示するビュー。"""

    def __init__(
        self,
        prompts: List[Prompt],
        on_restore: Optional[Callable[[Prompt], None]] = None,
        on_permanent_delete: Optional[Callable[[Prompt], None]] = None,
        on_empty_trash: Optional[Callable[[], None]] = None,
    ):
        self.prompts = prompts
        self._on_restore = on_restore
        self._on_permanent_delete = on_permanent_delete
        self._on_empty_trash = on_empty_trash

        super().__init__(
            content=self._build_content(),
            expand=True,
            padding=PADDING_MD,
        )

    def _build_content(self) -> ft.Control:
        """ビューコンテンツを構築する。"""
        if not self.prompts:
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.DELETE_OUTLINE, size=64, color="#606060"),
                        ft.Text(
                            "ゴミ箱は空です",
                            size=16,
                            color="#808080",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                expand=True,
                alignment=ft.Alignment(0, 0),
            )

        # ヘッダー（ゴミ箱を空にするボタン）
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        f"{len(self.prompts)}件のアイテム",
                        size=14,
                        color=TEXT_SECONDARY,
                    ),
                    ft.Container(expand=True),
                    ft.TextButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.DELETE_FOREVER, size=16, color=ERROR_COLOR),
                                ft.Text("ゴミ箱を空にする", color=ERROR_COLOR),
                            ],
                            spacing=4,
                        ),
                        on_click=lambda _: self._on_empty_trash() if self._on_empty_trash else None,
                    ),
                ],
            ),
            padding=ft.padding.only(bottom=16),
        )

        # カードグリッド
        cards = [
            TrashCard(
                prompt=prompt,
                on_restore=self._on_restore,
                on_permanent_delete=self._on_permanent_delete,
            )
            for prompt in self.prompts
        ]

        grid = ft.Row(
            controls=cards,
            wrap=True,
            spacing=CARD_GAP,
            run_spacing=CARD_GAP,
        )

        return ft.Column(
            controls=[header, grid],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
