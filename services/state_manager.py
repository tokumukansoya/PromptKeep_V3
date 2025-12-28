"""状態管理サービス。

アプリケーションの状態を一元管理し、デバウンス付き自動保存を提供する。
"""

import asyncio
from typing import Callable, List, Optional

from models.app_state import AppState
from models.prompt import Prompt
from models.category import Category
from services.data_service import DataService
from config import DEBOUNCE_SECONDS
from utils.logger import logger

# 型エイリアス
StateListener = Callable[[AppState], None]


class StateManager:
    """Singleton的なアプリケーション状態管理クラス。

    全ての状態変更はこのクラスを経由する。
    デバウンス付き自動保存機能を提供。

    Attributes:
        data_service: データ永続化サービス
        debounce_seconds: 保存デバウンス時間（秒）
    """

    def __init__(
        self,
        data_service: DataService,
        debounce_seconds: float = DEBOUNCE_SECONDS,
    ) -> None:
        """初期化。

        Args:
            data_service: データ永続化サービス
            debounce_seconds: 保存デバウンス時間
        """
        self.data_service = data_service
        self.debounce_seconds = debounce_seconds
        self._state: AppState = AppState.empty()
        self._listeners: List[StateListener] = []
        self._save_task: Optional[asyncio.Task] = None

    @property
    def state(self) -> AppState:
        """現在の状態を取得する。"""
        return self._state

    def add_listener(self, listener: StateListener) -> None:
        """状態変更時のリスナーを追加する。

        Args:
            listener: 状態変更時に呼び出されるコールバック
        """
        self._listeners.append(listener)

    def remove_listener(self, listener: StateListener) -> None:
        """リスナーを削除する。

        Args:
            listener: 削除するリスナー
        """
        if listener in self._listeners:
            self._listeners.remove(listener)

    def notify_listeners(self) -> None:
        """全てのリスナーに状態変更を通知する。"""
        for listener in self._listeners:
            try:
                listener(self._state)
            except Exception as e:
                logger.error(f"Listener error: {e}")

    def load(self) -> AppState:
        """データを読み込む。"""
        self._state = self.data_service.load()
        logger.info(f"State loaded: {len(self._state.prompts)} prompts, {len(self._state.categories)} categories")
        return self._state

    def save(self) -> None:
        """データを保存する。"""
        self.data_service.save(self._state)
        logger.info("State saved")

    async def _debounced_save(self) -> None:
        """デバウンス付きで保存する。"""
        await asyncio.sleep(self.debounce_seconds)
        self.save()

    def schedule_save(self) -> None:
        """デバウンス付き保存をスケジュールする。"""
        if self._save_task and not self._save_task.done():
            self._save_task.cancel()
        try:
            loop = asyncio.get_running_loop()
            self._save_task = loop.create_task(self._debounced_save())
        except RuntimeError:
            # イベントループがない場合は同期的に保存
            try:
                self.save()
            except Exception as e:
                logger.error(f"Failed to save synchronously: {e}")

    def update_state(self, **kwargs) -> None:
        """状態を更新し、リスナーに通知して保存をスケジュールする。"""
        for key, value in kwargs.items():
            if hasattr(self._state, key):
                setattr(self._state, key, value)
        self.notify_listeners()
        self.schedule_save()

    # プロンプト操作
    def add_prompt(self, prompt: Prompt) -> None:
        """プロンプトを追加する。"""
        self._state.prompts.append(prompt)
        self.notify_listeners()
        self.schedule_save()

    def update_prompt(self, prompt: Prompt) -> None:
        """プロンプトを更新する。"""
        for i, p in enumerate(self._state.prompts):
            if p.id == prompt.id:
                self._state.prompts[i] = prompt
                break
        self.notify_listeners()
        self.schedule_save()

    def remove_prompt(self, prompt_id: str) -> None:
        """プロンプトを完全に削除する。"""
        self._state.prompts = [p for p in self._state.prompts if p.id != prompt_id]
        self.notify_listeners()
        self.schedule_save()

    # カテゴリ操作
    def add_category(self, category: Category) -> None:
        """カテゴリを追加する。"""
        self._state.categories.append(category)
        self.notify_listeners()
        self.schedule_save()

    def update_category(self, category: Category) -> None:
        """カテゴリを更新する。"""
        for i, c in enumerate(self._state.categories):
            if c.id == category.id:
                self._state.categories[i] = category
                break
        self.notify_listeners()
        self.schedule_save()

    def remove_category(self, category_id: str) -> None:
        """カテゴリを削除する。"""
        self._state.categories = [c for c in self._state.categories if c.id != category_id]
        # プロンプトからもカテゴリIDを削除
        for prompt in self._state.prompts:
            if category_id in prompt.category_ids:
                prompt.category_ids.remove(category_id)
        self.notify_listeners()
        self.schedule_save()

    # 選択状態
    def select_category(self, category_id: Optional[str]) -> None:
        """カテゴリを選択する。"""
        self._state.selected_category_id = category_id
        self.notify_listeners()

    def set_search_query(self, query: str) -> None:
        """検索クエリを設定する。"""
        self._state.search_query = query
        self.notify_listeners()

    def set_editing_prompt(self, prompt_id: Optional[str]) -> None:
        """編集中のプロンプトを設定する。"""
        self._state.current_editing_id = prompt_id
        self.notify_listeners()