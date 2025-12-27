"""StateManager - アプリケーション状態管理の中核クラス。

状態の一元管理、自動保存、変更通知を担当。
Flet 0.28.3、Python 3.14.2 対応。
"""

import asyncio
from typing import TYPE_CHECKING, Callable, List, Optional

from loguru import logger

from models.app_state import AppState
from models.category import Category
from models.prompt import Prompt
from services.data_service import DataService

if TYPE_CHECKING:
    import flet as ft


class StateManager:
    """アプリケーション状態を管理する中核クラス。

    責務:
        - AppStateの一元管理
        - 状態変更時の自動保存（デバウンス付き）
        - UI更新通知の配信
        - データ永続化の統括

    Attributes:
        _page: Fletのpageオブジェクト（非同期タスク実行用）
        _state: 現在のアプリケーション状態
        _data_service: データ永続化サービス
        _listeners: 状態変更リスナーのリスト
        _save_task: 自動保存のタスク

    Note:
        - 全てのControllerはこのクラスを経由して状態を変更する
        - 状態を直接変更せず、必ずメソッドを呼ぶこと
        - 自動保存は2秒のデバウンス付き
        - 非同期処理はpage.run_task()を使用（asyncio.create_task()は使用しない）
    """

    def __init__(
        self,
        page: "ft.Page",
        data_service: DataService,
        debounce_seconds: float = 2.0,
    ):
        """StateManagerを初期化。

        Args:
            page: Fletのpageオブジェクト（非同期タスク実行用）
            data_service: データ永続化サービス
            debounce_seconds: 自動保存のデバウンス時間（秒）
        """
        self._page = page
        self._state = AppState.empty()
        self._data_service = data_service
        self._listeners: List[Callable[[AppState], None]] = []
        self._save_task: Optional[asyncio.Task] = None
        self._debounce_seconds = debounce_seconds
        logger.info("StateManager initialized")

    @property
    def state(self) -> AppState:
        """現在の状態を取得（読み取り専用）。

        Returns:
            現在のAppState
        """
        return self._state

    def load(self) -> None:
        """データをファイルから読み込む。

        Raises:
            DataPersistenceError: 読み込み失敗時
        """
        try:
            self._state = self._data_service.load()
            logger.info(
                f"State loaded: {len(self._state.prompts)} prompts, {len(self._state.categories)} categories"
            )
            self._notify_listeners()
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            raise

    def add_listener(self, listener: Callable[[AppState], None]) -> None:
        """状態変更リスナーを登録。

        Args:
            listener: 状態変更時に呼ばれるコールバック
        """
        self._listeners.append(listener)

    def remove_listener(self, listener: Callable[[AppState], None]) -> None:
        """状態変更リスナーを解除。

        Args:
            listener: 解除するコールバック
        """
        if listener in self._listeners:
            self._listeners.remove(listener)

    def update_prompts(self, prompts: List[Prompt]) -> None:
        """プロンプトリストを更新。

        Args:
            prompts: 新しいプロンプトリスト
        """
        self._state.prompts = prompts
        self._notify_listeners()
        self._schedule_save()

    def update_categories(self, categories: List[Category]) -> None:
        """カテゴリリストを更新。

        Args:
            categories: 新しいカテゴリリスト
        """
        self._state.categories = categories
        self._notify_listeners()
        self._schedule_save()

    def set_selected_category(self, category_id: str | None) -> None:
        """選択中のカテゴリを設定。

        Args:
            category_id: カテゴリID（None = 全表示）
        """
        self._state.selected_category_id = category_id
        self._notify_listeners()

    def set_search_query(self, query: str) -> None:
        """検索クエリを設定。

        Args:
            query: 検索文字列
        """
        self._state.search_query = query
        self._notify_listeners()

    def set_editing_prompt(self, prompt_id: str | None) -> None:
        """編集中のプロンプトを設定。

        Args:
            prompt_id: プロンプトID（None = 編集なし）
        """
        self._state.current_editing_id = prompt_id
        self._notify_listeners()

    def _notify_listeners(self) -> None:
        """全てのリスナーに状態変更を通知。"""
        for listener in self._listeners:
            try:
                listener(self._state)
            except Exception as e:
                logger.error(f"Listener error: {e}")

    def _schedule_save(self) -> None:
        """自動保存をスケジュール（デバウンス付き）。

        Flet推奨: page.run_task()を使用（asyncio.create_task()は使用しない）
        """
        if self._save_task:
            self._save_task.cancel()

        # Flet推奨パターン: page.run_task()でバックグラウンドタスク実行
        self._save_task = self._page.run_task(self._debounced_save)

    async def _debounced_save(self) -> None:
        """デバウンス付き自動保存。"""
        try:
            await asyncio.sleep(self._debounce_seconds)
            self._save()
        except asyncio.CancelledError:
            # キャンセルされた場合は何もしない
            pass

    def _save(self) -> None:
        """状態をファイルに保存。

        Raises:
            DataPersistenceError: 保存失敗時
        """
        try:
            self._data_service.save(self._state)
            logger.info("State saved successfully")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
            raise

    def force_save(self) -> None:
        """即座に保存（デバウンスなし）。

        アプリ終了時などに使用。
        """
        if self._save_task:
            self._save_task.cancel()
        self._save()
