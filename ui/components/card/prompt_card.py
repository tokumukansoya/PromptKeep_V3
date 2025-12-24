from __future__ import annotations

from typing import Callable

import flet as ft

from models.prompt import Prompt
from ui.components.card.card_header import CardHeader
from ui.components.card.card_body import CardBody
from ui.styles.card_style import (
    CARD_WIDTH,
    CARD_HEIGHT,
    CARD_BG_COLOR,
    CARD_BORDER_COLOR,
    CARD_BORDER_WIDTH,
    CARD_BORDER_RADIUS,
    CARD_PADDING,
    CARD_HOVER_OPACITY,
)
from utils.text_utils import truncate_preview


class PromptCard(ft.Container):
    """プロンプトカード全体コンポーネント。

    上部ヘッダー（お気に入り/コピー）＋本文（タイトル/プレビュー）で構成される正方形カード。
    Flet 0.28.3 API 準拠。

    Attributes:
        prompt: 表示対象の `Prompt` データ。
        on_click: カードクリック時のコールバック。
        on_copy: コピー操作時のコールバック。
        on_toggle_favorite: お気に入りトグル時のコールバック。
    """

    def __init__(
        self,
        prompt: Prompt,
        on_click: Callable[[ft.ControlEvent, Prompt], None],
        on_copy: Callable[[ft.ControlEvent, Prompt], None],
        on_toggle_favorite: Callable[[ft.ControlEvent, Prompt], None],
    ) -> None:
        """初期化。

        Args:
            prompt: 表示する `Prompt`。
            on_click: カードクリック時に呼ばれるコールバック（`e`, `prompt`）。
            on_copy: ヘッダーコピークリック時に呼ばれるコールバック（`e`, `prompt`）。
            on_toggle_favorite: ヘッダーお気に入りトグル時に呼ばれるコールバック（`e`, `prompt`）。
        """
        super().__init__()
        self.prompt: Prompt = prompt
        self._on_click: Callable[[ft.ControlEvent, Prompt], None] = on_click
        self._on_copy: Callable[[ft.ControlEvent, Prompt], None] = on_copy
        self._on_toggle_favorite: Callable[[ft.ControlEvent, Prompt], None] = (
            on_toggle_favorite
        )

        # ヘッダー: コールバックは Prompt を束縛するラッパーを渡す
        header: CardHeader = CardHeader(
            is_favorite=self.prompt.favorite,
            on_copy=lambda e: self._on_copy(e, self.prompt),
            on_toggle_favorite=lambda e: self._on_toggle_favorite(e, self.prompt),
        )

        # 本文: タイトル + プレビュー
        body: CardBody = CardBody(
            title=self.prompt.title,
            body_preview=truncate_preview(self.prompt.body),
        )

        # カードコンテンツ（縦積み）
        content_column: ft.Column = ft.Column(
            controls=[header, body],
            spacing=8,
            tight=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )

        # スタイル適用
        self.content = content_column
        self.width = CARD_WIDTH
        self.height = CARD_HEIGHT
        self.padding = ft.padding.all(CARD_PADDING)
        self.bgcolor = CARD_BG_COLOR
        self.border = ft.border.all(CARD_BORDER_WIDTH, CARD_BORDER_COLOR)
        self.border_radius = ft.border_radius.all(CARD_BORDER_RADIUS)
        self.opacity = 1.0

        # インタラクション
        self.on_click = self._handle_click
        self.on_hover = self._handle_hover

    def _handle_click(self, e: ft.ControlEvent) -> None:
        """カードクリックイベントハンドラ。

        Args:
            e: Flet のコントロールイベント。
        """
        self._on_click(e, self.prompt)

    def _handle_hover(self, e: ft.HoverEvent) -> None:
        """ホバー時の透明度変更。

        Args:
            e: ホバーイベント（`e.data` が "true"/"false"）。
        """
        is_hover: bool = str(e.data).lower() == "true"
        self.opacity = CARD_HOVER_OPACITY if is_hover else 1.0
        try:
            self.update()
        except AssertionError:
            # ページ未アタッチ時（テスト等）は update をスキップ
            pass

    def build(self) -> ft.Container:  # type: ignore[override]
        """Flet ビルド関数。

        Returns:
            ft.Container: 自身のコンテナを返します。
        """
        return self
