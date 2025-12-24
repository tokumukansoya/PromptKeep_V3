from __future__ import annotations

from typing import Callable

import flet as ft

from ui.styles import colors, spacing


class CardHeader(ft.Row):
    """カードヘッダー（お気に入りトグル + コピー）。

    左にお気に入り★、右にコピーアイコンボタンを配置します。
    Flet 0.28.3 API 準拠。

    Attributes:
        is_favorite: 初期のお気に入り状態。
        on_copy: コピー実行時のコールバック。
        on_toggle_favorite: お気に入りトグル時のコールバック。
    """

    def __init__(
        self,
        is_favorite: bool,
        on_copy: Callable[[ft.ControlEvent], None],
        on_toggle_favorite: Callable[[ft.ControlEvent], None],
    ) -> None:
        """初期化。

        Args:
            is_favorite: 初期のお気に入り状態。
            on_copy: コピーボタン押下時に呼ばれるコールバック。
            on_toggle_favorite: お気に入りトグル時に呼ばれるコールバック。
        """
        self._is_favorite: bool = is_favorite
        self._on_copy: Callable[[ft.ControlEvent], None] = on_copy
        self._on_toggle_favorite: Callable[[ft.ControlEvent], None] = on_toggle_favorite

        # 左: お気に入りトグル
        self._favorite_btn: ft.IconButton = ft.IconButton(
            icon=ft.Icons.STAR if self._is_favorite else ft.Icons.STAR_BORDER,
            icon_color=(
                colors.STAR_FILLED if self._is_favorite else colors.STAR_UNFILLED
            ),
            icon_size=spacing.ICON_SIZE,
            tooltip="お気に入り",
            on_click=self._handle_toggle_favorite,
            style=ft.ButtonStyle(padding=0),
        )

        # 右: コピー
        self._copy_btn: ft.IconButton = ft.IconButton(
            icon=ft.Icons.CONTENT_COPY,
            icon_size=spacing.ICON_SIZE,
            tooltip="コピー",
            on_click=self._handle_copy,
            style=ft.ButtonStyle(padding=0),
        )

        # レイアウト: 左右端に配置（間は可変スペーサ）
        spacer: ft.Container = ft.Container(expand=True)

        super().__init__(
            controls=[self._favorite_btn, spacer, self._copy_btn],
            spacing=0,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _handle_copy(self, e: ft.ControlEvent) -> None:
        """コピークリックの内部ハンドラ。

        Args:
            e: Flet のコントロールイベント。
        """
        self._on_copy(e)

    def _handle_toggle_favorite(self, e: ft.ControlEvent) -> None:
        """お気に入りトグルの内部ハンドラ（楽観的 UI 更新）。

        親コールバックへイベントを渡しつつ、即時に見た目を更新します。

        Args:
            e: Flet のコントロールイベント。
        """
        # 楽観的トグル（UI 即時反映）
        self._is_favorite = not self._is_favorite
        self._favorite_btn.icon = (
            ft.Icons.STAR if self._is_favorite else ft.Icons.STAR_BORDER
        )
        self._favorite_btn.icon_color = (
            colors.STAR_FILLED if self._is_favorite else colors.STAR_UNFILLED
        )
        try:
            self.update()
        except AssertionError:
            # ページ未アタッチ時（テスト等）は update をスキップ
            pass

        # コールバック呼び出し
        self._on_toggle_favorite(e)

    def build(self) -> ft.Row:  # type: ignore[override]
        """Flet ビルド関数。

        Returns:
            ft.Row: 自身の行コンテナを返します。
        """
        return self
