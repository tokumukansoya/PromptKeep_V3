from __future__ import annotations

from typing import Callable, Optional

import flet as ft

from models.app_state import AppState
from models.prompt import Prompt
from ui.components.sidebar.sidebar import Sidebar
from ui.styles import colors, spacing
from ui.views.card_grid_view import CardGridView
from ui.views.edit_view import EditView
from ui.controllers.main_controller import MainController
from ui.controllers.edit_controller import EditController
from ui.controllers.category_controller import CategoryController


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
        main_controller: MainController,
        edit_controller: EditController,
        category_controller: Optional[CategoryController],
        on_view_change: Callable[[], None],
    ) -> None:
        """初期化。

        Args:
            state: アプリケーション全体の状態。
            on_view_change: ビュー変更時のコールバック。
        """
        super().__init__()

        self._state: AppState = state
        self._main_controller: MainController = main_controller
        self._edit_controller: EditController = edit_controller
        self._category_controller: Optional[CategoryController] = category_controller
        self._on_view_change: Callable[[], None] = on_view_change

        # 起動時にフィルタをクリアし、最低1件の編集対象を用意
        self._main_controller.clear_filters(self._state)
        self._ensure_prompt_exists()

        # サイドバーの生成
        self._sidebar: Sidebar = Sidebar(
            categories=self._state.categories,
            on_search=self._handle_search,
            on_category_select=self._handle_category_select,
            on_clear_selection=self._handle_clear_selection,
            on_category_add=self._handle_category_add,
            on_category_move=self._handle_category_move,
            initial_query=self._state.search_query,
        )
        self._sidebar_container = ft.Container(
            content=self._sidebar,
            width=300,  # サイドバー固定幅：20-30% を想定
            padding=spacing.GAP_MD,
            bgcolor=colors.DARK_BG_SECONDARY,
        )

        # コンテンツエリア（CardGridView または EditView をここに配置）
        self._content_container: ft.Container = ft.Container(
            expand=True,
            content=self._build_content(),
        )

        # 右下に新規プロンプト追加ボタン（Floating Action）
        add_prompt_button = ft.FloatingActionButton(
            icon="add",
            tooltip="新規プロンプト",
            on_click=self._handle_add_prompt,
        )
        floating_add = ft.Container(
            content=add_prompt_button,
            alignment=ft.alignment.bottom_right,
            padding=spacing.GAP_MD,
        )

        # Row レイアウト：左 (Sidebar 20-30%) | 右 (Content 70-80%)
        self.controls = [
            self._sidebar_container,
            ft.Stack(controls=[self._content_container, floating_add], expand=True),
        ]
        self.spacing = 0
        self.expand = True

    def _refresh_sidebar(self) -> None:
        """サイドバーを最新の状態で再構築して更新する。"""
        try:
            self._sidebar = Sidebar(
                categories=self._state.categories,
                on_search=self._handle_search,
                on_category_select=self._handle_category_select,
                on_clear_selection=self._handle_clear_selection,
                on_category_add=self._handle_category_add,
                on_category_move=self._handle_category_move,
                initial_query=self._state.search_query,
            )
            self._sidebar_container.content = self._sidebar
            self._sidebar_container.update()
        except Exception:
            return

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
        # MainController のフィルタリングを使用
        return self._main_controller.get_filtered_prompts(self._state)

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
        self._main_controller.on_search(self._state, query)
        self._update_content()

    def _handle_category_select(self, category) -> None:
        """カテゴリ選択時をハンドル。

        Args:
            category: 選択されたカテゴリ。
        """
        self._main_controller.on_category_change(self._state, category.id)
        self._update_content()

    def _handle_clear_selection(self) -> None:
        """カテゴリ選択を全解除する。"""
        try:
            self._sidebar.clear_search()
        except Exception:
            pass
        self._main_controller.clear_filters(self._state)
        self._update_content()

    def _handle_category_add(self) -> None:
        """カテゴリ追加ボタンクリック時をハンドル。

        実装詳細はコントローラーで処理。
        現状はデフォルト名で追加。
        """
        try:
            if self._category_controller:
                # デフォルト名で現在選択カテゴリ配下に追加
                parent_id = self._state.selected_category_id
                self._category_controller.on_add_category(
                    self._state, name="新規カテゴリ", parent_id=parent_id
                )
                self._refresh_sidebar()
                self._update_content()
        except Exception:
            # 失敗時は無視（Snackbar はコントローラー側で表示）
            return

    def _handle_category_move(self, source_id: str, target_parent_id: str) -> None:
        """カテゴリ移動（DnD）時をハンドル。

        Args:
            source_id: 移動元カテゴリ ID。
            target_parent_id: 移動先親カテゴリ ID。
        """
        # 実装詳細はコントローラーで処理
        # TODO: CategoryController に対応するメソッドを実装後に接続
        return

    def _handle_card_click(self, e: ft.ControlEvent, prompt: Prompt) -> None:
        """カードクリック時をハンドル。

        Args:
            e: Flet イベント。
            prompt: クリックされたプロンプト。
        """
        self._main_controller.on_card_click(self._state, prompt.id)
        self._update_content()

    def _handle_copy(self, e: ft.ControlEvent, prompt: Prompt) -> None:
        """コピーボタンクリック時をハンドル。

        Args:
            e: Flet イベント。
            prompt: コピー対象のプロンプト。
        """
        if self.page:
            self._main_controller.on_copy_prompt(self.page, prompt)

    def _handle_toggle_favorite(self, e: ft.ControlEvent, prompt: Prompt) -> None:
        """お気に入りトグル時をハンドル。

        Args:
            e: Flet イベント。
            prompt: トグル対象のプロンプト。
        """
        self._main_controller.on_toggle_favorite(self._state, prompt.id)
        self._update_content()

    def _handle_save(self, title: str, body: str, category_path: list) -> None:
        """EditView からの保存をハンドル。

        Args:
            title: 編集後のタイトル。
            body: 編集後の本文。
            category_path: 編集後のカテゴリパス。
        """
        try:
            if self._state.current_editing_id:
                self._edit_controller.on_save(
                    self._state,
                    self._state.current_editing_id,
                    title,
                    body,
                    category_path,
                )
        except Exception:
            return

    def _handle_back(self) -> None:
        """EditView からの戻るボタンをハンドル。

        編集ビューから カードグリッドビューに戻ります。
        """
        try:
            self._edit_controller.on_back(self._navigate_back_to_grid)
        except Exception:
            self._navigate_back_to_grid()

    def _handle_add_prompt(self, _: ft.ControlEvent) -> None:
        """新規プロンプト追加ボタンのハンドラ。"""
        try:
            self._sidebar.clear_search()
        except Exception:
            pass
        self._main_controller.clear_filters(self._state)
        self._main_controller.on_add_prompt(self._state)
        self._update_content()

    def refresh(self) -> None:
        """状態変更後にサイドバーとコンテンツを再構成する。"""
        try:
            self._refresh_sidebar()
            self._update_content()
        except Exception:
            return

    def _update_content(self) -> None:
        """コンテンツエリアを再構成。

        状態の変更を反映して、CardGridView または EditView を切り替えます。
        """
        self._content_container.content = self._build_content()
        self._content_container.update()
        if self.page:
            try:
                self.page.update()
            except Exception:
                pass

    def _navigate_back_to_grid(self) -> None:
        """編集ビューからカードグリッドへ戻る内部ユーティリティ。"""
        self._state.current_editing_id = None
        self._update_content()

    def build(self) -> ft.Row:  # type: ignore[override]
        """Flet ビルド関数。

        Returns:
            ft.Row: 自身のインスタンスを返します。
        """
        return self

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def _ensure_prompt_exists(self) -> None:
        """初回起動時、プロンプトが1件もない場合にダミーを作成して編集状態にする。"""
        if self._state.prompts:
            return
        self._main_controller.on_add_prompt(self._state)
        self._update_content()
