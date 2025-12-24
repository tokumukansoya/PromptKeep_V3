from __future__ import annotations

import flet as ft

from ui.styles import colors, typography, spacing
from utils.text_utils import truncate_preview


class CardBody(ft.Container):
    """カード本文（タイトル + 本文プレビュー）コンポーネント。

    タイトルは1行・太字、プレビューは複数行可で `utils.text_utils.truncate_preview()` により
    指定長へ切り詰められます。Flet 0.28.3 API 準拠。

    Attributes:
        title: カードのタイトルテキスト。
        body_preview: 本文のプレビュー元テキスト。
    """

    def __init__(self, title: str, body_preview: str) -> None:
        """初期化。

        Args:
            title: タイトル文字列。
            body_preview: プレビュー生成対象の本文文字列。
        """
        super().__init__()

        # 生成済みのテキストコントロールを保持
        title_text: ft.Text = ft.Text(
            value=title,
            color=colors.TEXT_PRIMARY,
            size=typography.FONT_SIZE_TITLE,
            weight=typography.FONT_WEIGHT_BOLD,
            font_family=typography.FONT_FAMILY,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

        preview_text: ft.Text = ft.Text(
            value=truncate_preview(body_preview),
            color=colors.TEXT_SECONDARY,
            size=typography.FONT_SIZE_BODY,
            weight=typography.FONT_WEIGHT_NORMAL,
            font_family=typography.FONT_FAMILY,
            # 複数行可、カードサイズに応じて自動折返し
            # 明示的な max_lines は指定しない
        )

        # レイアウト: タイトル上、プレビュー下
        content_column: ft.Column = ft.Column(
            controls=[title_text, preview_text],
            spacing=spacing.GAP_SM,
            tight=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        # コンテナ自体のスタイリング
        self.content = content_column
        self.padding = ft.padding.all(spacing.PADDING_MD)
        self.bgcolor = colors.TRANSPARENT  # 背景は親カード側で指定

    def build(self) -> ft.Container:  # type: ignore[override]
        """Flet ビルド関数。

        Returns:
            ft.Container: 自身のコンテナを返します。
        """
        return self
