from __future__ import annotations

import asyncio
from typing import Callable, List, Optional

import flet as ft

from config import AUTOSAVE_DEBOUNCE_MS
from models.category import Category
from models.prompt import Prompt
from ui.components.editor.body_field import BodyField
from ui.components.editor.category_selector import CategorySelector
from ui.components.editor.editor_toolbar import EditorToolbar
from ui.components.editor.title_field import TitleField
from ui.styles import spacing


class EditView(ft.Column):
    """プロンプト編集ビュー（自動保存付き）。"""

    def __init__(
        self,
        prompt: Prompt,
        categories: List[Category],
        on_save: Callable[[str, str, List[str]], None],
        on_back: Callable[[], None],
    ) -> None:
        """初期化。

        Args:
            prompt: 編集対象のプロンプト。
            categories: カテゴリ一覧。
            on_save: 自動保存時に (title, body, category_path) を渡すコールバック。
            on_back: 戻るボタンクリック時のコールバック。
        """
        super().__init__()
        self._prompt = prompt
        self._categories = categories
        self._on_save: Callable[[str, str, List[str]], None] = on_save
        self._on_back: Callable[[], None] = on_back

        self._title: str = prompt.title
        self._body: str = prompt.body
        self._category_path: List[str] = list(prompt.category_path)

        self._debounce_task: Optional[asyncio.Task[None]] = None

        toolbar = EditorToolbar(on_back=self._handle_back)
        title_field = TitleField(value=self._title, on_change=self._handle_title_change)
        body_field = BodyField(value=self._body, on_change=self._handle_body_change)
        category_selector = CategorySelector(
            categories=self._categories,
            selected_path=self._category_path,
            on_change=self._handle_category_change,
        )

        self.controls = [
            toolbar,
            title_field,
            body_field,
            category_selector,
        ]
        self.spacing = spacing.GAP_MD
        self.expand = True
        self.alignment = ft.MainAxisAlignment.START

    def _handle_back(self) -> None:
        """戻るボタンクリック時のハンドラ。"""
        self._on_back()

    def _handle_title_change(self, value: str) -> None:
        """タイトル変更時に内部状態を更新し保存をスケジュール。"""
        self._title = value
        self._schedule_save()

    def _handle_body_change(self, value: str) -> None:
        """本文変更時に内部状態を更新し保存をスケジュール。"""
        self._body = value
        self._schedule_save()

    def _handle_category_change(self, path: List[str]) -> None:
        """カテゴリ変更時に内部状態を更新し保存をスケジュール。"""
        self._category_path = path
        self._schedule_save()

    def _schedule_save(self) -> None:
        """デバウンス付きで自動保存をスケジュールする。"""
        if self._debounce_task and not self._debounce_task.done():
            self._debounce_task.cancel()
        self._debounce_task = asyncio.create_task(self._debounced_save())

    async def _debounced_save(self) -> None:
        """デバウンス時間経過後に保存を呼び出す。"""
        try:
            await asyncio.sleep(AUTOSAVE_DEBOUNCE_MS / 1000)
            self._emit_save()
        except asyncio.CancelledError:
            return

    def _emit_save(self) -> None:
        """現在の値で on_save コールバックを実行する。"""
        try:
            result = self._on_save(self._title, self._body, self._category_path)
            if asyncio.iscoroutine(result):
                asyncio.create_task(result)
        except Exception:
            # ここでは握りつぶし、上位でエラー処理する場合は適宜拡張
            return

    def build(self) -> ft.Column:  # type: ignore[override]
        """Flet ビルド関数。"""
        return self
