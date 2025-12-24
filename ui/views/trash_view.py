from __future__ import annotations

from typing import Callable, List

import flet as ft

from models.prompt import Prompt
from ui.styles import colors, spacing, typography


class TrashView(ft.Column):
    """ゴミ箱ビュー（削除済みプロンプト一覧）。

    上部に「ゴミ箱を空にする」ボタン、中央に削除済みプロンプトの
    一覧を表示します。各アイテムには「復元」ボタンを配置します。

    Flet 0.28.3 の API を使用。

    Args:
        deleted_prompts: 削除済み `Prompt` の一覧。
        on_restore: 個別アイテムの復元ハンドラ。`(e, prompt)` を受け取る。
        on_empty: ゴミ箱を空にするハンドラ。確認後に呼び出される（`e` を受け取る）。

    Attributes:
        _deleted_prompts: 表示対象の削除済みプロンプト一覧。
        _on_restore: 復元時に呼び出すコールバック。
        _on_empty: ゴミ箱を空にする実行コールバック。
        _list_view: 削除済みリストの `ListView`。
        _confirm_dialog: ゴミ箱を空にする確認 `AlertDialog`。
    """

    def __init__(
        self,
        deleted_prompts: List[Prompt],
        on_restore: Callable[[ft.ControlEvent, Prompt], None],
        on_empty: Callable[[ft.ControlEvent], None],
    ) -> None:
        """初期化。

        Args:
            deleted_prompts: 削除済み `Prompt` の一覧。
            on_restore: 復元ハンドラ（`(e, prompt)`）。
            on_empty: ゴミ箱を空にするハンドラ（確認後に呼び出し、`(e,)`）。
        """
        super().__init__()

        self._deleted_prompts: List[Prompt] = deleted_prompts
        self._on_restore = on_restore
        self._on_empty = on_empty

        # ヘッダ（上部の操作エリア）
        self._header = self._build_header()

        # リストビュー（中央の削除済み一覧）
        self._list_view = self._build_list()

        # レイアウト設定
        self.controls = [self._header, self._list_view]
        self.spacing = spacing.GAP_LG
        self.expand = True

        # 確認ダイアログのテンプレート（必要時に page にアタッチ）
        self._confirm_dialog = self._build_confirm_dialog()

    # ---------------------------------------------------------------------
    # UI builders
    # ---------------------------------------------------------------------
    def _build_header(self) -> ft.Container:
        """ヘッダー（ゴミ箱操作領域）を構築する。

        Returns:
            Flet コンテナ（ヘッダー行）。
        """
        empty_button = ft.ElevatedButton(
            text="ゴミ箱を空にする",
            icon="delete_forever_rounded",
            bgcolor=colors.ERROR_COLOR,
            color=colors.TEXT_PRIMARY,
            on_click=self._handle_empty_click,
            height=spacing.BUTTON_HEIGHT,
        )
        header = ft.Row(
            controls=[
                ft.Text(
                    value="ゴミ箱",
                    size=typography.FONT_SIZE_HEADING,
                    color=colors.TEXT_PRIMARY,
                ),
                ft.Container(expand=True),
                empty_button,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        return ft.Container(
            content=header,
            padding=spacing.PADDING_LG,
            bgcolor=colors.DARK_BG_SECONDARY,
        )

    def _build_list(self) -> ft.Control:
        """削除済みプロンプト一覧を構築する。

        Returns:
            `ft.ListView` または空状態の `ft.Container`。
        """
        if not self._deleted_prompts:
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(
                            name="delete_outline_rounded",
                            color=colors.TEXT_SECONDARY,
                            size=48,
                        ),
                        ft.Text(
                            value="ゴミ箱は空です",
                            color=colors.TEXT_SECONDARY,
                            size=typography.FONT_SIZE_SUBTITLE,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=spacing.GAP_MD,
                ),
                expand=True,
            )

        items: List[ft.Control] = []
        for p in self._deleted_prompts:
            items.append(self._build_list_item(p))

        return ft.ListView(
            controls=items,
            spacing=0,
            auto_scroll=False,
            expand=True,
        )

    def _build_list_item(self, prompt: Prompt) -> ft.Container:
        """削除済みプロンプトの 1 アイテム行を構築する。

        Args:
            prompt: 対象の `Prompt`。

        Returns:
            行コンテナ。
        """
        title = ft.Text(
            value=prompt.title or "(無題)",
            size=typography.FONT_SIZE_TITLE,
            color=colors.TEXT_PRIMARY,
            no_wrap=True,
        )
        subtitle = ft.Text(
            value=(prompt.body or "").replace("\n", " ")[:120],
            size=typography.FONT_SIZE_BODY,
            color=colors.TEXT_SECONDARY,
            max_lines=2,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        restored_btn = ft.TextButton(
            text="復元",
            icon="restore_from_trash_rounded",
            on_click=lambda e, _p=prompt: self._on_restore(e, _p),
        )
        row = ft.Row(
            controls=[
                ft.Column(
                    controls=[title, subtitle],
                    spacing=spacing.GAP_XS,
                    expand=True,
                ),
                restored_btn,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        return ft.Container(
            content=row,
            padding=spacing.PADDING_LG,
            border=ft.border.all(1, colors.BORDER_COLOR),
            border_radius=spacing.BORDER_RADIUS_MD,
            bgcolor=colors.DARK_BG_SECONDARY,
            margin=ft.margin.only(
                left=spacing.MARGIN_LG, right=spacing.MARGIN_LG, top=spacing.MARGIN_MD
            ),
        )

    def _build_confirm_dialog(self) -> ft.AlertDialog:
        """ゴミ箱を空にする確認ダイアログを構築する。

        Returns:
            `ft.AlertDialog` のインスタンス。
        """

        def _close(_: ft.ControlEvent | None = None) -> None:
            if self.page:
                self._confirm_dialog.open = False
                self.page.update()

        def _confirm(e: ft.ControlEvent) -> None:
            # 実行してから閉じる
            try:
                self._on_empty(e)
            finally:
                _close()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("確認", color=colors.TEXT_PRIMARY),
            content=ft.Text(
                "ゴミ箱を空にします。よろしいですか？", color=colors.TEXT_SECONDARY
            ),
            actions=[
                ft.TextButton("キャンセル", on_click=_close),
                ft.ElevatedButton(
                    "空にする",
                    icon="delete_forever_rounded",
                    bgcolor=colors.ERROR_COLOR,
                    on_click=_confirm,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return dialog

    # ---------------------------------------------------------------------
    # Events
    # ---------------------------------------------------------------------
    def _handle_empty_click(self, e: ft.ControlEvent) -> None:
        """「ゴミ箱を空にする」ボタンクリック時のハンドラ。

        Args:
            e: Flet のイベント。
        """
        if not self.page:
            return
        # ページのオーバーレイにダイアログを追加して開く
        try:
            if self._confirm_dialog not in self.page.overlay:
                self.page.overlay.append(self._confirm_dialog)
            self._confirm_dialog.open = True
            self.page.update()
        except Exception:
            # 失敗しても致命的ではないため無視
            return

    # ---------------------------------------------------------------------
    # Flet lifecycle
    # ---------------------------------------------------------------------
    def build(self) -> ft.Column:  # type: ignore[override]
        """Flet ビルド関数。

        Returns:
            自身（`ft.Column`）。
        """
        return self
