"""PromptKeep アプリケーション。

メインアプリケーションクラスとUI構築を担当。
"""

import flet as ft
from flet import Page, ThemeMode
from typing import Optional, List

from models.prompt import Prompt
from models.category import Category
from services.data_service import DataService
from services.state_manager import StateManager
from services.prompt_service import PromptService
from services.category_service import CategoryService
from ui.components.sidebar.sidebar import Sidebar
from ui.views.card_grid_view import CardGridView
from ui.views.edit_view import EditView
from ui.views.trash_view import TrashView
from ui.styles.colors import DARK_BG_PRIMARY, DARK_BG_SECONDARY, TEXT_PRIMARY, ACCENT_PRIMARY
from utils.logger import logger


# ビューモード定数
VIEW_MODE_ALL = "all"
VIEW_MODE_FAVORITES = "favorites"
VIEW_MODE_TRASH = "trash"
VIEW_MODE_CATEGORY = "category"


class PromptKeepApp:
    """PromptKeep アプリケーションクラス。

    プロンプト管理アプリのメインエントリーポイント。
    UIの構築、イベントハンドリング、状態管理を統括する。

    Attributes:
        title: ウィンドウタイトル
        page: FletのPageインスタンス
        view_mode: 現在のビューモード
        is_editing: 編集モードかどうか
    """

    # ウィンドウ設定定数
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    MIN_WINDOW_WIDTH = 800
    MIN_WINDOW_HEIGHT = 600

    def __init__(self) -> None:
        """アプリケーションの初期化。"""
        self.title = "PromptKeep"

        # サービス初期化
        self.data_service = DataService()
        self.state_manager = StateManager(self.data_service)
        self.prompt_service = PromptService()
        self.category_service = CategoryService()

        # UI状態
        self.view_mode = VIEW_MODE_ALL
        self.editing_prompt: Optional[Prompt] = None
        self.is_editing = False
        self.page: Optional[Page] = None
        self.search_query = ""

    def run(self) -> None:
        """Fletアプリケーションを起動する。"""

        def on_page_load(page: Page) -> None:
            """ページ読み込み時の初期化処理。"""
            self.page = page
            self._configure_window(page)
            self._load_data()
            self._setup_listeners()
            self._build_ui()

        ft.app(target=on_page_load, view=ft.AppView.WEB_BROWSER)

    def _configure_window(self, page: Page) -> None:
        """ウィンドウを設定する。

        Args:
            page: FletのPageインスタンス
        """
        page.title = self.title
        page.window.width = self.WINDOW_WIDTH
        page.window.height = self.WINDOW_HEIGHT
        page.window.min_width = self.MIN_WINDOW_WIDTH
        page.window.min_height = self.MIN_WINDOW_HEIGHT

        # ダークテーマ固定
        page.theme_mode = ThemeMode.DARK
        page.bgcolor = DARK_BG_PRIMARY
        page.theme = ft.Theme(
            color_scheme_seed=ft.Colors.BLUE,
            visual_density=ft.VisualDensity.COMFORTABLE,
        )
        page.padding = 0
        page.spacing = 0

    def _load_data(self) -> None:
        """データを読み込む。"""
        try:
            self.state_manager.load()
            logger.info("Data loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load data: {e}")

    def _setup_listeners(self) -> None:
        """イベントリスナーを設定する。"""
        self.state_manager.add_listener(lambda _: self._refresh_ui())

    def _build_ui(self) -> None:
        """UIを構築する。"""
        if not self.page:
            return

        self.page.controls.clear()

        # メインレイアウト
        main_layout = ft.Row(
            controls=[
                self._build_sidebar(),
                ft.VerticalDivider(width=1, color="#3A3A3A"),
                self._build_main_content(),
            ],
            expand=True,
            spacing=0,
        )

        self.page.add(main_layout)
        self.page.update()

    def _build_sidebar(self) -> Sidebar:
        """サイドバーを構築する。"""
        state = self.state_manager.state

        # プロンプト数をカウント
        prompt_counts = {
            "all": len(state.get_active_prompts()),
            "favorites": len(state.get_favorite_prompts()),
            "trash": len(state.get_trashed_prompts()),
        }

        # カテゴリ別のカウント
        for category in state.categories:
            prompt_counts[category.id] = len(state.get_prompts_by_category(category.id))

        return Sidebar(
            categories=state.categories,
            selected_category_id=state.selected_category_id,
            prompt_counts=prompt_counts,
            view_mode=self.view_mode,
            on_show_all=self._show_all,
            on_show_favorites=self._show_favorites,
            on_show_trash=self._show_trash,
            on_category_select=self._select_category,
            on_add_category=self._show_add_category_dialog,
            on_delete_category=self._show_delete_category_dialog,
        )

    def _build_main_content(self) -> ft.Container:
        """メインコンテンツを構築する。"""
        if self.is_editing:
            return ft.Container(
                content=EditView(
                    prompt=self.editing_prompt,
                    categories=self.state_manager.state.categories,
                    on_save=self._save_prompt,
                    on_cancel=self._cancel_edit,
                    is_new=self.editing_prompt is None,
                ),
                expand=True,
            )

        # ヘッダー
        header = self._build_header()

        # ゴミ箱ビューの場合
        if self.view_mode == "trash":
            prompts = self.state_manager.state.get_trashed_prompts()
            content_view = TrashView(
                prompts=prompts,
                on_restore=self._restore_prompt,
                on_permanent_delete=self._show_permanent_delete_dialog,
                on_empty_trash=self._show_empty_trash_dialog,
            )
        else:
            # カードグリッド
            prompts = self._get_filtered_prompts()
            content_view = CardGridView(
                prompts=prompts,
                on_card_click=self._edit_prompt,
                on_copy=lambda p: None,  # コピーはカード内で処理
                on_favorite=self._toggle_favorite,
                on_delete=self._delete_prompt,
            )

        return ft.Container(
            content=ft.Column(
                controls=[header, content_view],
                expand=True,
                spacing=0,
            ),
            expand=True,
            bgcolor=DARK_BG_PRIMARY,
        )

    def _build_header(self) -> ft.Container:
        """ヘッダーを構築する。

        Returns:
            ヘッダーのコンテナ
        """
        state = self.state_manager.state

        # タイトルの決定
        title_map = {
            VIEW_MODE_ALL: "すべてのプロンプト",
            VIEW_MODE_FAVORITES: "お気に入り",
            VIEW_MODE_TRASH: "ゴミ箱",
        }
        if self.view_mode in title_map:
            title = title_map[self.view_mode]
        else:
            category = state.get_category_by_id(state.selected_category_id)
            title = category.name if category else "プロンプト"

        # 検索フィールド（クリアボタン付き）
        search_field = ft.TextField(
            hint_text="検索...",
            value=self.search_query,
            prefix_icon=ft.Icons.SEARCH,
            suffix=ft.IconButton(
                icon=ft.Icons.CLEAR,
                icon_size=16,
                tooltip="クリア",
                on_click=self._clear_search,
            ) if self.search_query else None,
            width=300,
            height=40,
            border_radius=20,
            on_submit=self._on_search_submit,
        )

        # コントロールリスト
        controls = [
            ft.Text(title, size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
            ft.Container(expand=True),
            search_field,
        ]

        # ゴミ箱以外のビューでは新規作成ボタンを表示
        if self.view_mode != VIEW_MODE_TRASH:
            controls.append(ft.Container(width=16))
            controls.append(
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ADD, size=18),
                            ft.Text("新規作成"),
                        ],
                        spacing=4,
                    ),
                    on_click=lambda _: self._new_prompt(),
                    bgcolor=ACCENT_PRIMARY,
                    color=TEXT_PRIMARY,
                )
            )

        return ft.Container(
            content=ft.Row(
                controls=controls,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=20,
            bgcolor=DARK_BG_SECONDARY,
        )

    def _get_filtered_prompts(self) -> List[Prompt]:
        """現在のビューモードに応じたプロンプトを取得する。

        Returns:
            フィルタリング済みのプロンプトリスト
        """
        state = self.state_manager.state

        # ビューモードに応じたプロンプト取得
        if self.view_mode == VIEW_MODE_ALL:
            prompts = state.get_active_prompts()
        elif self.view_mode == VIEW_MODE_FAVORITES:
            prompts = state.get_favorite_prompts()
        elif self.view_mode == VIEW_MODE_TRASH:
            prompts = state.get_trashed_prompts()
        else:
            prompts = state.get_prompts_by_category(state.selected_category_id)

        # 検索フィルタ
        if self.search_query:
            prompts = self.prompt_service.search_prompts(prompts, self.search_query)

        return prompts

    def _refresh_ui(self) -> None:
        """UIを再描画する。"""
        self._build_ui()

    # ナビゲーションイベントハンドラ
    def _show_all(self) -> None:
        """すべてのプロンプトを表示する。"""
        self.view_mode = VIEW_MODE_ALL
        self.state_manager.select_category(None)
        self._refresh_ui()

    def _show_favorites(self) -> None:
        """お気に入りを表示する。"""
        self.view_mode = VIEW_MODE_FAVORITES
        self.state_manager.select_category(None)
        self._refresh_ui()

    def _show_trash(self) -> None:
        """ゴミ箱を表示する。"""
        self.view_mode = VIEW_MODE_TRASH
        self.state_manager.select_category(None)
        self._refresh_ui()

    def _select_category(self, category_id: str) -> None:
        """カテゴリを選択する。

        Args:
            category_id: 選択するカテゴリID
        """
        self.view_mode = VIEW_MODE_CATEGORY
        self.state_manager.select_category(category_id)
        self._refresh_ui()

    def _on_search_submit(self, e: ft.ControlEvent) -> None:
        """検索テキスト確定時の処理。"""
        self.search_query = e.control.value
        self._refresh_ui()

    def _clear_search(self, e: ft.ControlEvent) -> None:
        """検索をクリアする。"""
        self.search_query = ""
        self._refresh_ui()

    def _new_prompt(self) -> None:
        """新規プロンプト作成を開始する。"""
        self.editing_prompt = None
        self.is_editing = True
        self._refresh_ui()

    def _edit_prompt(self, prompt: Prompt) -> None:
        """プロンプトの編集を開始する。"""
        self.editing_prompt = prompt
        self.is_editing = True
        self._refresh_ui()

    def _save_prompt(self, title: str, body: str, category_ids: List[str]) -> None:
        """プロンプトを保存する。"""
        if self.editing_prompt:
            # 更新
            self.prompt_service.update_prompt(
                self.editing_prompt,
                title=title,
                body=body,
                category_ids=category_ids,
            )
            self.state_manager.update_prompt(self.editing_prompt)
        else:
            # 新規作成
            prompt = self.prompt_service.create_prompt(title, body, category_ids)
            self.state_manager.add_prompt(prompt)

        self.is_editing = False
        self.editing_prompt = None
        self._refresh_ui()

        # 通知
        self._show_snackbar("保存しました")

    def _cancel_edit(self) -> None:
        """編集をキャンセルする。"""
        self.is_editing = False
        self.editing_prompt = None
        self._refresh_ui()

    def _toggle_favorite(self, prompt: Prompt) -> None:
        """お気に入り状態をトグルする。"""
        self.prompt_service.toggle_favorite(prompt)
        self.state_manager.update_prompt(prompt)

    def _delete_prompt(self, prompt: Prompt) -> None:
        """プロンプトを削除する（ゴミ箱へ）。"""
        self.prompt_service.delete_prompt(prompt)
        self.state_manager.update_prompt(prompt)
        self._show_snackbar("ゴミ箱に移動しました")

    def _restore_prompt(self, prompt: Prompt) -> None:
        """プロンプトをゴミ箱から復元する。"""
        self.prompt_service.restore_prompt(prompt)
        self.state_manager.update_prompt(prompt)
        self._show_snackbar("復元しました")

    def _permanent_delete_prompt(self, prompt: Prompt) -> None:
        """プロンプトを完全に削除する。"""
        self.state_manager.remove_prompt(prompt.id)
        self._show_snackbar("完全に削除しました")

    def _show_permanent_delete_dialog(self, prompt: Prompt) -> None:
        """完全削除確認ダイアログを表示する。"""
        if not self.page:
            return

        def close_dialog(e=None):
            dialog.open = False
            self.page.update()

        def confirm_delete(e):
            close_dialog()
            self._permanent_delete_prompt(prompt)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("完全に削除しますか？"),
            content=ft.Text(f"「{prompt.title}」を完全に削除します。\nこの操作は取り消せません。"),
            actions=[
                ft.TextButton(content=ft.Text("キャンセル"), on_click=close_dialog),
                ft.ElevatedButton(
                    content=ft.Text("削除"),
                    on_click=confirm_delete,
                    bgcolor="#F44336",
                    color=TEXT_PRIMARY,
                ),
            ],
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _show_empty_trash_dialog(self) -> None:
        """ゴミ箱を空にする確認ダイアログを表示する。"""
        if not self.page:
            return

        trashed = self.state_manager.state.get_trashed_prompts()
        if not trashed:
            self._show_snackbar("ゴミ箱は空です")
            return

        def close_dialog(e=None):
            dialog.open = False
            self.page.update()

        def confirm_empty(e):
            close_dialog()
            for prompt in trashed:
                self.state_manager.remove_prompt(prompt.id)
            self._show_snackbar("ゴミ箱を空にしました")

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("ゴミ箱を空にしますか？"),
            content=ft.Text(f"{len(trashed)}件のプロンプトを完全に削除します。\nこの操作は取り消せません。"),
            actions=[
                ft.TextButton(content=ft.Text("キャンセル"), on_click=close_dialog),
                ft.ElevatedButton(
                    content=ft.Text("空にする"),
                    on_click=confirm_empty,
                    bgcolor="#F44336",
                    color=TEXT_PRIMARY,
                ),
            ],
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _show_add_category_dialog(self) -> None:
        """カテゴリ追加ダイアログを表示する。"""
        if not self.page:
            return

        name_field = ft.TextField(
            label="カテゴリ名",
            autofocus=True,
        )

        def close_dialog(e=None):
            dialog.open = False
            self.page.update()

        def save_category(e):
            name = name_field.value.strip()
            if name:
                category = self.category_service.create_category(name)
                self.state_manager.add_category(category)
                close_dialog()
                self._show_snackbar("カテゴリを追加しました")

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("カテゴリを追加"),
            content=name_field,
            actions=[
                ft.TextButton(content=ft.Text("キャンセル"), on_click=close_dialog),
                ft.ElevatedButton(content=ft.Text("追加"), on_click=save_category),
            ],
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _show_delete_category_dialog(self, category: Category) -> None:
        """カテゴリ削除確認ダイアログを表示する。"""
        if not self.page:
            return

        # このカテゴリに属するプロンプト数を取得
        prompts_in_category = self.state_manager.state.get_prompts_by_category(category.id)
        prompt_count = len(prompts_in_category)

        def close_dialog(e=None):
            dialog.open = False
            self.page.update()

        def confirm_delete(e):
            close_dialog()
            self.state_manager.remove_category(category.id)
            # 選択中のカテゴリだった場合は「すべて」に戻る
            if self.state_manager.state.selected_category_id == category.id:
                self.view_mode = VIEW_MODE_ALL
                self.state_manager.select_category(None)
            self._show_snackbar("カテゴリを削除しました")

        content_text = f"「{category.name}」を削除します。"
        if prompt_count > 0:
            content_text += f"\n\nこのカテゴリには{prompt_count}件のプロンプトがあります。\nプロンプトは削除されず、カテゴリのみ削除されます。"

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("カテゴリを削除しますか？"),
            content=ft.Text(content_text),
            actions=[
                ft.TextButton(content=ft.Text("キャンセル"), on_click=close_dialog),
                ft.ElevatedButton(
                    content=ft.Text("削除"),
                    on_click=confirm_delete,
                    bgcolor="#F44336",
                    color=TEXT_PRIMARY,
                ),
            ],
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _show_snackbar(self, message: str) -> None:
        """スナックバーを表示する。"""
        if not self.page:
            return
        snack = ft.SnackBar(content=ft.Text(message), duration=1500)
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()