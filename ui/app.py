from __future__ import annotations

import logging
from typing import Optional

import flet as ft

from config import WINDOW_WIDTH, WINDOW_HEIGHT, APP_VERSION
from models.app_state import AppState
from services.data_service import DataService
from services.prompt_service import PromptService
from services.category_service import CategoryService
from services.clipboard_service import ClipboardService
from services.search_service import SearchService
from services.undo_service import UndoService
from ui.controllers.main_controller import MainController
from ui.controllers.edit_controller import EditController
from ui.controllers.category_controller import CategoryController
from ui.controllers.keyboard_controller import KeyboardController
from ui.views.main_view import MainView
from ui.styles import colors

logger = logging.getLogger(__name__)


class PromptKeepApp:
    """PromptKeep Flet アプリケーション。

    Flet ベースのデスクトップアプリケーション。
    すべてのサービスとUI層を統合し、メイン画面を表示する。

    Attributes:
        _data_service: データ永続化サービス。
        _prompt_service: プロンプトサービス。
        _category_service: カテゴリサービス。
        _clipboard_service: クリップボードサービス。
        _search_service: 検索サービス。
        _main_controller: メインコントローラー。
        _state: アプリケーション状態。

    Note:
        - Flet 0.28.3 API 対応。
        - ダークテーマを使用。
        - Python 3.14.2 対応。

    Example:
        >>> app = PromptKeepApp()
        >>> app.run()
    """

    def __init__(self) -> None:
        """PromptKeepApp の初期化。

        各サービスをインスタンス化し、メインコントローラーを生成。
        AppState をファイルから読み込む。
        """
        logger.info(f"PromptKeepApp initializing (version: {APP_VERSION})")

        # サービスのインスタンス化
        self._data_service = DataService()
        self._prompt_service = PromptService(self._data_service)
        self._category_service = CategoryService(self._data_service)
        self._clipboard_service = ClipboardService()
        self._search_service = SearchService()
        self._undo_service = UndoService()

        # AppState の読み込み
        self._state: AppState = self._data_service.load()
        logger.info(
            f"Loaded state: {len(self._state.prompts)} prompts, "
            f"{len(self._state.categories)} categories"
        )

        # コントローラー生成
        self._main_controller = MainController(
            prompt_service=self._prompt_service,
            category_service=self._category_service,
            data_service=self._data_service,
            clipboard_service=self._clipboard_service,
            search_service=self._search_service,
            undo_service=self._undo_service,
        )
        self._edit_controller = EditController(
            prompt_service=self._prompt_service, data_service=self._data_service
        )
        self._category_controller = CategoryController(
            category_service=self._category_service, data_service=self._data_service
        )
        self._keyboard_controller: Optional[KeyboardController] = None

        logger.debug("PromptKeepApp initialized successfully")

    def run(self) -> None:
        """アプリケーションを実行。

        Flet アプリケーションをビルドして実行。

        Returns:
            None

        Note:
            - この呼び出しはブロッキング操作。
            - アプリケーション終了まで制御が戻らない。
        """
        logger.info("Starting PromptKeepApp")
        ft.app(target=self.main)

    def main(self, page: ft.Page) -> None:
        """Flet メイン関数。

        Page を初期化し、メインビューを配置して表示する。

        Args:
            page: Flet Page インスタンス。

        Returns:
            None

        Note:
            - このメソッドは ft.app() から呼び出される。
            - Page の全設定をここで行う。
        """
        logger.info("Building main page")

        # ============================================================================
        # Page 基本設定
        # ============================================================================
        page.title = "PromptKeep"
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.START

        # ============================================================================
        # テーマ設定
        # ============================================================================
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = colors.DARK_BG

        # ============================================================================
        # ウィンドウ設定
        # ============================================================================
        # Flet 0.28.3 では window プロパティを通じて設定
        page.window.width = WINDOW_WIDTH
        page.window.height = WINDOW_HEIGHT
        page.window.min_width = 800
        page.window.min_height = 600

        # ============================================================================
        # コントローラーの Page 関連付け
        # ============================================================================
        self._main_controller.attach_page(page)
        self._category_controller.attach_page(page)
        self._edit_controller.attach_page(page)

        # ============================================================================
        # メインビューの生成と追加
        # ============================================================================
        try:
            main_view = MainView(
                state=self._state,
                main_controller=self._main_controller,
                edit_controller=self._edit_controller,
                category_controller=self._category_controller,
                on_view_change=lambda: self._on_view_changed(page, main_view),
            )
            page.add(main_view)
            logger.info("Main view added to page")

            self._keyboard_controller = KeyboardController(
                page=page,
                undo_handler=lambda: self._main_controller.undo_last_operation(
                    self._state
                ),
                on_state_restored=lambda: self._refresh_ui(main_view),
            )
            self._keyboard_controller.setup_shortcuts()
        except Exception as e:
            logger.error(f"Failed to build main view: {e}")
            page.clean()
            error_text = ft.Text(
                f"アプリケーションの初期化に失敗しました: {e}",
                color=colors.ERROR_COLOR,
            )
            page.add(error_text)

    def _on_view_changed(self, page: ft.Page, main_view: MainView) -> None:
        """ビュー変更時のコールバック。

        UI を再更新する処理をここに記述。

        Args:
            page: Flet Page インスタンス。
            main_view: メインビューインスタンス。

        Returns:
            None

        Note:
            - 状態変更に応じて UI を更新。
            - 必要に応じてページ全体をリフレッシュ。
        """
        try:
            logger.debug("View changed callback triggered")
            # UI 更新の実装（必要に応じて）
            # main_view.update() など
            page.update()
        except Exception as e:
            logger.error(f"Failed to handle view change: {e}")

    def _refresh_ui(self, main_view: MainView) -> None:
        """アンドゥ適用後などに UI を再構成する。"""
        try:
            main_view.refresh()
        except Exception as e:
            logger.error(f"Failed to refresh UI after undo: {e}")


def main() -> None:
    """エントリーポイント。

    ログ設定、アプリケーション起動を行う。

    Returns:
        None

    Note:
        - このモジュールが直接実行される場合に呼ばれる。
        - main.py から呼び出される。
    """
    # ログレベルを DEBUG に設定
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger.info(f"PromptKeep Application (version {APP_VERSION})")
    app = PromptKeepApp()
    app.run()


if __name__ == "__main__":
    main()
