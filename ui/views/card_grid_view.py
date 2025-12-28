"""カードグリッドビュー。"""

import flet as ft
from typing import Callable, List, Optional

from models.prompt import Prompt
from ui.components.card.prompt_card import PromptCard
from ui.styles.spacing import CARD_GAP, PADDING_MD


class CardGridView(ft.Container):
    """プロンプトカードをグリッド表示するビュー。"""

    def __init__(
        self,
        prompts: List[Prompt],
        on_card_click: Optional[Callable[[Prompt], None]] = None,
        on_copy: Optional[Callable[[Prompt], None]] = None,
        on_favorite: Optional[Callable[[Prompt], None]] = None,
        on_delete: Optional[Callable[[Prompt], None]] = None,
    ):
        self.prompts = prompts
        self._on_card_click = on_card_click
        self._on_copy = on_copy
        self._on_favorite = on_favorite
        self._on_delete = on_delete

        super().__init__(
            content=self._build_content(),
            expand=True,
            padding=PADDING_MD,
        )

    def _build_content(self) -> ft.Control:
        """グリッドコンテンツを構築する。"""
        if not self.prompts:
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.DESCRIPTION, size=64, color="#606060"),
                        ft.Text(
                            "プロンプトがありません",
                            size=16,
                            color="#808080",
                        ),
                        ft.Text(
                            "「+ 新規作成」ボタンでプロンプトを追加しましょう",
                            size=12,
                            color="#606060",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                expand=True,
                alignment=ft.Alignment(0, 0),
            )

        cards = [
            PromptCard(
                prompt=prompt,
                on_click=self._on_card_click,
                on_copy=self._on_copy,
                on_favorite=self._on_favorite,
                on_delete=self._on_delete,
            )
            for prompt in self.prompts
        ]

        return ft.Column(
            controls=[
                ft.Row(
                    controls=cards,
                    wrap=True,
                    spacing=CARD_GAP,
                    run_spacing=CARD_GAP,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
