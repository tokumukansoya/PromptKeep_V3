from __future__ import annotations

from typing import Callable, List

import flet as ft

from config import CARD_SIZE
from models.prompt import Prompt
from ui.components.card.prompt_card import PromptCard
from ui.styles import spacing


class CardGridView(ft.GridView):
    """カードグリッドビュー。

    `PromptCard` をグリッド状に並べ、画面幅に応じて列数（`runs_count`）を調整します。
    Flet 0.28.3 API 準拠。

    Attributes:
        prompts: 表示対象の `Prompt` リスト。
        on_card_click: カードクリック時のコールバック（`e`, `prompt`）。
        on_copy: コピークリック時のコールバック（`e`, `prompt`）。
        on_toggle_favorite: お気に入りトグル時のコールバック（`e`, `prompt`）。
    """

    def __init__(
        self,
        prompts: List[Prompt],
        on_card_click: Callable[[ft.ControlEvent, Prompt], None],
        on_copy: Callable[[ft.ControlEvent, Prompt], None],
        on_toggle_favorite: Callable[[ft.ControlEvent, Prompt], None],
    ) -> None:
        """初期化。

        Args:
            prompts: 表示する `Prompt` の一覧。
            on_card_click: カードクリック時に呼ばれるコールバック（`e`, `prompt`）。
            on_copy: コピークリック時に呼ばれるコールバック（`e`, `prompt`）。
            on_toggle_favorite: お気に入りトグル時に呼ばれるコールバック（`e`, `prompt`）。
        """
        self._prompts: List[Prompt] = prompts
        self._on_card_click = on_card_click
        self._on_copy = on_copy
        self._on_toggle_favorite = on_toggle_favorite

        # カード生成
        controls: List[ft.Control] = [
            PromptCard(
                prompt=p,
                on_click=self._on_card_click,
                on_copy=self._on_copy,
                on_toggle_favorite=self._on_toggle_favorite,
            )
            for p in self._prompts
        ]

        # 初期レイアウト設定
        super().__init__(
            controls=controls,
            spacing=spacing.GAP_MD,  # 子要素間の間隔
            run_spacing=spacing.GAP_MD,  # 行間の間隔
            child_aspect_ratio=1.0,  # 子要素が正方形想定
            auto_scroll=False,
            expand=True,
        )

        # 初期列数計算（ページ未アタッチ時は仮計算）
        self.runs_count = self._calc_runs_count()

    def _calc_runs_count(self) -> int:
        """現在のページ幅から列数を計算。

        Returns:
            int: 列数（最低 1）。
        """
        width_attr = getattr(self.page, "window_width", 0.0) if self.page else 0.0
        try:
            width: float = float(width_attr)
        except Exception:
            width = 0.0
        if width <= 0:
            # ページ未アタッチなどで幅不明な場合は 3 列を仮採用
            return max(1, int(3))
        # 丸めて列数算出（最低 1 列）
        cols = max(1, int(width // CARD_SIZE))
        return cols

    def build(self) -> ft.GridView:  # type: ignore[override]
        """Flet ビルド関数。

        Returns:
            ft.GridView: 自身のグリッドビューを返します。
        """
        # ページアタッチ後にも列数を再計算して反映
        try:
            self.runs_count = self._calc_runs_count()
        except Exception:
            # 計算失敗時は既定値維持
            pass
        return self
