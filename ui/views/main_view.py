from __future__ import annotations

from typing import Callable, Optional

import flet as ft

from models.app_state import AppState
from models.prompt import Prompt
from ui.components.sidebar.sidebar import Sidebar
from ui.styles import colors, spacing
from ui.views.card_grid_view import CardGridView
from ui.views.edit_view import EditView


class MainView(ft.Row):
    """メイン画面全体のレイアウト。

    左側にサイドバー、右側にカードグリッド表示または編集ビューを
    水平分割で配置します。`state.current_editing_id` に応じて表示を切り替えます。

    Args:
        state: アプリケーション全体の状態。
        on_view_change: ビュー変更時のコールバック（必要に応じて呼び出し）。

    Attributes:
        _state: 現在のアプリケーション状態。
        _on_view_change: ビュー変更時のコールバック。

    Note:
        - Flet 0.28.3 API 対応。
        - Row で水平分割：Sidebar (20-30%) | Content (70-80%)。
        - state.current_editing_id が None のとき CardGridView を表示。
        - state.current_editing_id が指定されているとき EditView を表示。
    """

    def __init__(
        self,
        state: AppState,
        on_view_change: Callable[[], None],
    ) -> None:
        """初期化。

        Args:
            state: アプリケーション全体の状態。
            on_view_change: ビュー変更時のコールバック。
        """
        super().__init__()

        self._state: AppState = state
        self._on_view_change: Callable[[], None] = on_view_change

        # サイドバーの生成
        self._sidebar: Sidebar = Sidebar(
            categories=self._state.categories,
            on_search=self._handle_search,
            on_category_select=self._handle_category_select,
            on_category_add=self._handle_category_add,
            on_category_move=self._handle_category_move,
        )

        # コンテンツエリア（CardGridView または EditView をここに配置）
        self._content_container: ft.Container = ft.Container(
            expand=True,
            content=self._build_content(),
        )

        # Row レイアウト：左 (Sidebar 20-30%) | 右 (Content 70-80%)
        self.controls = [
            ft.Container(
                content=self._sidebar,
                width=300,  # サイドバー固定幅：20-30% を想定
                padding=spacing.GAP_MD,
                bgcolor=colors.DARK_BG_SECONDARY,
            ),
            self._content_container,
        ]
        self.spacing = 0
        self.expand = True

    def _build_content(self) -> ft.Control:
        """編集状態に応じてコンテンツビューを生成。

        Returns:
            ft.Control: CardGridView または EditView。
        """
        if self._state.current_editing_id is None:
            # CardGridView を表示
            return CardGridView(
                prompts=self._get_filtered_prompts(),
                on_card_click=self._handle_card_click,
                on_copy=self._handle_copy,
                on_toggle_favorite=self._handle_toggle_favorite,
            )
        else:
            # EditView を表示
            prompt = self._find_prompt_by_id(self._state.current_editing_id)
            if prompt is None:
                # プロンプトが見つからない場合は CardGridView にフォールバック
                return CardGridView(
                    prompts=self._get_filtered_prompts(),
                    on_card_click=self._handle_card_click,
                    on_copy=self._handle_copy,
                    on_toggle_favorite=self._handle_toggle_favorite,
                )
            return EditView(
                prompt=prompt,
                categories=self._state.categories,
                on_save=self._handle_save,
                on_back=self._handle_back,
            )

    def _get_filtered_prompts(self):
        """カテゴリおよび検索クエリでフィルタリングされたプロンプト一覧を取得。

        Returns:
            list: フィルタリング済みのプロンプト一覧。
        """
        # ここでは簡略版：実際の実装は SearchService などを使用
        prompts = self._state.prompts
        # ゴミ箱内のプロンプトは除外
        prompts = [p for p in prompts if p.id not in self._state.trash]
        # カテゴリフィルタ（実装例）
        if self._state.selected_category_id is not None:
            # selected_category_id に基づいてフィルタ（簡略版）
            pass
        # 検索クエリフィルタ（実装例）
        if self._state.search_query:
            # search_query に基づいてフィルタ（簡略版）
            pass
        return prompts

    def _find_prompt_by_id(self, prompt_id: str) -> Optional[Prompt]:
        """プロンプト ID からプロンプトを検索。

        Args:
            prompt_id: プロンプト ID。

        Returns:
            Prompt: 見つかったプロンプト、見つからない場合は None。
        """
        for p in self._state.prompts:
            if p.id == prompt_id:
                return p
        return None

    def _handle_search(self, query: str) -> None:
        """検索ボックスの変更をハンドル。

        Args:
            query: 検索クエリ。
        """
        # 状態を更新（実装詳細はコントローラーで処理）
        # self._state.search_query = query
        # コンテンツを再生成
        self._update_content()

    def _handle_category_select(self, category) -> None:
        """カテゴリ選択時をハンドル。

        Args:
            category: 選択されたカテゴリ。
        """
        # 状態を更新（実装詳細はコントローラーで処理）
        # self._state.selected_category_id = category.id
        # コンテンツを再生成
        self._update_content()

    def _handle_category_add(self) -> None:
        """カテゴリ追加ボタンクリック時をハンドル。

        実装詳細はコントローラーで処理。
        """
        pass

    def _handle_category_move(self, source_id: str, target_parent_id: str) -> None:
        """カテゴリ移動（DnD）時をハンドル。

        Args:
            source_id: 移動元カテゴリ ID。
            target_parent_id: 移動先親カテゴリ ID。
        """
        # 実装詳細はコントローラーで処理
        pass

    def _handle_card_click(self, e: ft.ControlEvent, prompt: Prompt) -> None:
        """カードクリック時をハンドル。

        Args:
            e: Flet イベント。
            prompt: クリックされたプロンプト。
        """
        # 状態を更新（実装詳細はコントローラーで処理）
        # self._state.current_editing_id = prompt.id
        # ビューを切り替え
        self._update_content()

    def _handle_copy(self, e: ft.ControlEvent, prompt: Prompt) -> None:
        """コピーボタンクリック時をハンドル。

        Args:
            e: Flet イベント。
            prompt: コピー対象のプロンプト。
        """
        # 実装詳細はコントローラーで処理
        pass

    def _handle_toggle_favorite(self, e: ft.ControlEvent, prompt: Prompt) -> None:
        """お気に入りトグル時をハンドル。

        Args:
            e: Flet イベント。
            prompt: トグル対象のプロンプト。
        """
        # 実装詳細はコントローラーで処理
        pass

    def _handle_save(self, title: str, body: str, category_path: list) -> None:
        """EditView からの保存をハンドル。

        Args:
            title: 編集後のタイトル。
            body: 編集後の本文。
            category_path: 編集後のカテゴリパス。
        """
        # 実装詳細はコントローラーで処理
        pass

    def _handle_back(self) -> None:
        """EditView からの戻るボタンをハンドル。

        編集ビューから カードグリッドビューに戻ります。
        """
        # 状態を更新（実装詳細はコントローラーで処理）
        # self._state.current_editing_id = None
        # ビューを切り替え
        self._update_content()

    def _update_content(self) -> None:
        """コンテンツエリアを再構成。

        状態の変更を反映して、CardGridView または EditView を切り替えます。
        """
        self._content_container.content = self._build_content()
        self._content_container.update()

    def build(self) -> ft.Row:  # type: ignore[override]
        """Flet ビルド関数。

        Returns:
            ft.Row: 自身のインスタンスを返します。
        """
        return self
