"""プロンプト編集ビュー。

プロンプトの新規作成・編集画面を提供する。
"""

import flet as ft
from typing import Callable, List, Optional

from models.prompt import Prompt
from models.category import Category
from ui.styles.colors import (
    DARK_BG_SECONDARY,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BORDER_COLOR,
    ACCENT_PRIMARY,
)
from ui.styles.spacing import PADDING_LG, BORDER_RADIUS_MD
from ui.styles.typography import FONT_SIZE_H2


class EditView(ft.Container):
    """プロンプト編集ビュー。

    タイトル、本文、カテゴリの編集機能を提供する。
    未保存変更がある場合は確認ダイアログを表示する。

    Attributes:
        prompt: 編集対象のプロンプト（新規の場合はNone）
        categories: 選択可能なカテゴリのリスト
        is_new: 新規作成モードかどうか
    """

    def __init__(
        self,
        prompt: Optional[Prompt] = None,
        categories: Optional[List[Category]] = None,
        on_save: Optional[Callable[[str, str, List[str]], None]] = None,
        on_cancel: Optional[Callable[[], None]] = None,
        is_new: bool = False,
    ) -> None:
        """初期化。

        Args:
            prompt: 編集対象のプロンプト（新規の場合はNone）
            categories: 選択可能なカテゴリのリスト
            on_save: 保存時のコールバック（title, body, category_ids）
            on_cancel: キャンセル時のコールバック
            is_new: 新規作成モードかどうか
        """
        self.prompt = prompt
        self.categories = categories or []
        self._on_save = on_save
        self._on_cancel = on_cancel
        self.is_new = is_new

        # 入力フィールド
        self.title_field = ft.TextField(
            label="タイトル",
            value=prompt.title if prompt else "",
            border_color=BORDER_COLOR,
            focused_border_color=ACCENT_PRIMARY,
            color=TEXT_PRIMARY,
            label_style=ft.TextStyle(color=TEXT_SECONDARY),
            on_change=self._on_field_change,
        )

        self.body_field = ft.TextField(
            label="本文",
            value=prompt.body if prompt else "",
            multiline=True,
            min_lines=10,
            max_lines=20,
            border_color=BORDER_COLOR,
            focused_border_color=ACCENT_PRIMARY,
            color=TEXT_PRIMARY,
            label_style=ft.TextStyle(color=TEXT_SECONDARY),
            expand=True,
            on_change=self._on_field_change,
        )

        # 初期値を保持（変更検出用）
        self._initial_title = prompt.title if prompt else ""
        self._initial_body = prompt.body if prompt else ""
        self._initial_category_ids = list(prompt.category_ids) if prompt else []
        self._has_changes = False

        # カテゴリ選択
        self.selected_category_ids = list(prompt.category_ids) if prompt else []
        self.category_chips = self._build_category_chips()

        super().__init__(
            content=self._build_content(),
            expand=True,
            bgcolor=DARK_BG_SECONDARY,
            border_radius=BORDER_RADIUS_MD,
            padding=PADDING_LG,
        )

    def _build_category_chips(self) -> ft.Row:
        """カテゴリ選択チップを構築する。"""
        chips = []
        for category in self.categories:
            is_selected = category.id in self.selected_category_ids
            chips.append(
                ft.Chip(
                    label=ft.Text(category.name),
                    selected=is_selected,
                    on_select=lambda e, c=category: self._toggle_category(c.id),
                )
            )
        return ft.Row(controls=chips, wrap=True, spacing=8)

    def _toggle_category(self, category_id: str) -> None:
        """カテゴリの選択をトグルする。"""
        if category_id in self.selected_category_ids:
            self.selected_category_ids.remove(category_id)
        else:
            self.selected_category_ids.append(category_id)
        self._has_changes = True
        self.category_chips = self._build_category_chips()
        self.content = self._build_content()
        self.update()

    def _on_field_change(self, e: ft.ControlEvent) -> None:
        """フィールド変更時の処理。"""
        self._has_changes = self._check_has_changes()

    def _check_has_changes(self) -> bool:
        """変更があるかチェックする。"""
        if self.title_field.value != self._initial_title:
            return True
        if self.body_field.value != self._initial_body:
            return True
        if sorted(self.selected_category_ids) != sorted(self._initial_category_ids):
            return True
        return False

    def _build_content(self) -> ft.Column:
        """編集ビューの中身を構築する。"""
        # ヘッダー
        header = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    tooltip="戻る",
                    on_click=self._handle_back,
                ),
                ft.Text(
                    "新規作成" if self.is_new else "編集",
                    size=FONT_SIZE_H2,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY,
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SAVE, size=18),
                            ft.Text("保存"),
                        ],
                        spacing=4,
                    ),
                    on_click=self._handle_save,
                    bgcolor=ACCENT_PRIMARY,
                    color=TEXT_PRIMARY,
                ),
            ],
        )

        # カテゴリセクション
        category_section = ft.Column(
            controls=[
                ft.Text("カテゴリ", size=14, color=TEXT_SECONDARY),
                self.category_chips if self.categories else ft.Text(
                    "カテゴリがありません", size=12, color="#606060"
                ),
            ],
            spacing=8,
        )

        return ft.Column(
            controls=[
                header,
                ft.Divider(height=20, color=BORDER_COLOR),
                self.title_field,
                ft.Container(height=16),
                category_section,
                ft.Container(height=16),
                self.body_field,
            ],
            spacing=8,
            expand=True,
        )

    def _handle_save(self, e: ft.ControlEvent) -> None:
        """保存ボタンクリック時の処理。"""
        title = self.title_field.value.strip()
        body = self.body_field.value.strip()

        if not title:
            self.title_field.error_text = "タイトルを入力してください"
            self.title_field.update()
            return

        if self._on_save:
            self._on_save(title, body, self.selected_category_ids)

    def _handle_back(self, e: ft.ControlEvent) -> None:
        """戻るボタンクリック時の処理。"""
        # 変更がある場合は確認ダイアログを表示
        if self._check_has_changes():
            self._show_discard_dialog(e.control.page)
        else:
            if self._on_cancel:
                self._on_cancel()

    def _show_discard_dialog(self, page) -> None:
        """変更を破棄するか確認するダイアログを表示。"""
        def close_dialog(e=None):
            dialog.open = False
            page.update()

        def discard_changes(e):
            close_dialog()
            if self._on_cancel:
                self._on_cancel()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("変更を破棄しますか？"),
            content=ft.Text("保存されていない変更があります。\n変更を破棄して戻りますか？"),
            actions=[
                ft.TextButton(content=ft.Text("編集を続ける"), on_click=close_dialog),
                ft.ElevatedButton(
                    content=ft.Text("破棄"),
                    on_click=discard_changes,
                    bgcolor="#F44336",
                    color=TEXT_PRIMARY,
                ),
            ],
        )

        page.overlay.append(dialog)
        dialog.open = True
        page.update()
