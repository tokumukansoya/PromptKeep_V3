from __future__ import annotations

import logging
from typing import Callable, List, Optional, Tuple

import flet as ft

from models.app_state import AppState
from models.prompt import Prompt
from services.prompt_service import PromptService
from services.category_service import CategoryService
from services.data_service import DataService
from services.clipboard_service import ClipboardService
from services.search_service import SearchService
from services.undo_service import UndoService
from exceptions import PromptNotFoundError, CategoryNotFoundError
from ui.components.common.snackbar import show_snackbar
from ui.styles.colors import ERROR_COLOR, SUCCESS_COLOR

logger = logging.getLogger(__name__)


class MainController:
    """メイン画面のコントローラー。

    プロンプト追加、カード操作、カテゴリ変更、検索など
    メイン画面に関連する各種操作を仲介し、サービス呼び出しと
    永続化を行う。エラー時はスナックバーで通知する。

    Args:
        prompt_service: プロンプトの CRUD を提供するサービス。
        category_service: カテゴリの CRUD を提供するサービス。
        data_service: データ永続化を担当するサービス。
        clipboard_service: クリップボード操作を提供するサービス。
        search_service: 検索・フィルタを提供するサービス（オプション）。

    Attributes:
        _prompt_service: プロンプトサービス。
        _category_service: カテゴリサービス。
        _data_service: データサービス。
        _clipboard_service: クリップボードサービス。
        _search_service: 検索サービス。
        _page: Snackbar 表示用の Flet Page インスタンス。
    """

    def __init__(
        self,
        prompt_service: PromptService,
        category_service: CategoryService,
        data_service: DataService,
        clipboard_service: ClipboardService,
        search_service: Optional[SearchService] = None,
        undo_service: Optional[UndoService] = None,
    ) -> None:
        """MainController の初期化。

        Args:
            prompt_service: PromptService インスタンス。
            category_service: CategoryService インスタンス。
            data_service: DataService インスタンス。
            clipboard_service: ClipboardService インスタンス。
            search_service: SearchService インスタンス（未指定時は新規作成）。
        """
        self._prompt_service = prompt_service
        self._category_service = category_service
        self._data_service = data_service
        self._clipboard_service = clipboard_service
        self._search_service = search_service or SearchService()
        self._undo_service = undo_service
        self._page: Optional[ft.Page] = None
        logger.debug("MainController initialized")

    def attach_page(self, page: ft.Page) -> None:
        """Snackbar 表示用に Flet `Page` を関連付ける。

        Args:
            page: Flet Page インスタンス。
        """
        self._page = page

    def on_add_prompt(self, state: AppState) -> None:
        """新規プロンプトを追加する。

        新規プロンプトを作成し、デフォルト値で初期化。
        編集ビューへの遷移は呼び出し側で処理。

        Args:
            state: 現在のアプリケーション状態。

        Returns:
            None

        Note:
            - 新規プロンプトは空のタイトル・本文で作成。
            - 現在のカテゴリ選択を反映。
            - 作成後の状態は state.prompts に追加、保存される。
        """
        try:
            # デフォルト値でプロンプト作成
            category_path = (
                state.selected_category_id if state.selected_category_id else []
            )
            prompt = self._prompt_service.create_prompt(
                title="",
                body="",
                category_path=category_path if isinstance(category_path, list) else [],
            )
            state.prompts.append(prompt)
            state.current_editing_id = prompt.id
            self._save_with_recovery(state)
            logger.info(f"New prompt added: {prompt.id}")
        except Exception as e:
            logger.error(f"Failed to add prompt: {e}")
            if self._page:
                show_snackbar(
                    self._page, "プロンプトの追加に失敗しました", bgcolor=ERROR_COLOR
                )

    def on_card_click(self, state: AppState, prompt_id: str) -> None:
        """カードクリック時をハンドル。

        プロンプトを編集ビュー用に選択。

        Args:
            state: 現在のアプリケーション状態。
            prompt_id: クリックされたプロンプト ID。

        Returns:
            None
        """
        try:
            prompt = self._prompt_service.get_prompt(state, prompt_id)
            state.current_editing_id = prompt.id
            logger.info(f"Card clicked: {prompt_id}")
        except PromptNotFoundError as e:
            logger.error(f"Prompt not found on card click: {prompt_id}")
            if self._page:
                show_snackbar(self._page, str(e), bgcolor=ERROR_COLOR)
        except Exception as e:
            logger.error(f"Failed to handle card click: {e}")
            if self._page:
                show_snackbar(
                    self._page, "プロンプト選択に失敗しました", bgcolor=ERROR_COLOR
                )

    def on_delete_prompt(self, state: AppState, prompt_id: str) -> None:
        """プロンプトを削除（ゴミ箱移動）する。

        論理削除（ゴミ箱へ移動）を実行。

        Args:
            state: 現在のアプリケーション状態。
            prompt_id: 削除対象のプロンプト ID。

        Returns:
            None
        """
        try:
            if self._undo_service:
                try:
                    self._undo_service.push_state(state)
                except Exception as snapshot_err:
                    logger.warning(
                        "Failed to push undo snapshot before delete: %s", snapshot_err
                    )
            self._prompt_service.delete_prompt(state, prompt_id)
            # 編集中だった場合は編集ビューから脱出
            if state.current_editing_id == prompt_id:
                state.current_editing_id = None
            self._save_with_recovery(state)
            logger.info(f"Prompt deleted: {prompt_id}")
            if self._page:
                show_snackbar(
                    self._page, "プロンプトを削除しました", bgcolor=SUCCESS_COLOR
                )
        except PromptNotFoundError as e:
            logger.error(f"Prompt not found on delete: {prompt_id}")
            if self._page:
                show_snackbar(self._page, str(e), bgcolor=ERROR_COLOR)
        except Exception as e:
            logger.error(f"Failed to delete prompt '{prompt_id}': {e}")
            if self._page:
                show_snackbar(
                    self._page, "プロンプトの削除に失敗しました", bgcolor=ERROR_COLOR
                )

    def undo_last_operation(self, state: AppState) -> Tuple[bool, str]:
        """UndoService から直前のスナップショットを適用する。"""

        if not self._undo_service:
            logger.warning("Undo service is not configured")
            return False, "アンドゥ機能が利用できません"

        try:
            snapshot = self._undo_service.undo()
            if snapshot is None:
                logger.info("Undo requested but stack is empty")
                return False, "元に戻せる操作がありません"

            restored = AppState.from_dict(snapshot)

            state.prompts = restored.prompts
            state.categories = restored.categories
            state.trash = restored.trash
            state.selected_category_id = restored.selected_category_id
            state.search_query = restored.search_query
            state.current_editing_id = restored.current_editing_id

            self._save_with_recovery(state)
            logger.info("State restored from undo snapshot")
            return True, "元に戻しました"
        except Exception as exc:
            logger.exception("Failed to apply undo snapshot")
            return False, "元に戻し処理に失敗しました"

    def on_copy_prompt(self, page: ft.Page, prompt: Prompt) -> None:
        """プロンプト本文をクリップボードにコピーする。

        Args:
            page: Flet Page インスタンス。
            prompt: コピー対象のプロンプト。

        Returns:
            None
        """
        try:
            success = self._clipboard_service.copy_to_clipboard(page, prompt.body)
            if success:
                logger.info(f"Prompt copied to clipboard: {prompt.id}")
                show_snackbar(
                    page, "クリップボードにコピーしました", bgcolor=SUCCESS_COLOR
                )
            else:
                logger.warning(f"Failed to copy prompt to clipboard: {prompt.id}")
                show_snackbar(
                    page, "クリップボードへのコピーに失敗しました", bgcolor=ERROR_COLOR
                )
        except Exception as e:
            logger.error(f"Failed to copy prompt '{prompt.id}': {e}")
            show_snackbar(page, "コピーに失敗しました", bgcolor=ERROR_COLOR)

    def on_toggle_favorite(self, state: AppState, prompt_id: str) -> None:
        """プロンプトのお気に入り状態をトグルする。

        Args:
            state: 現在のアプリケーション状態。
            prompt_id: トグル対象のプロンプト ID。

        Returns:
            None
        """
        try:
            self._prompt_service.toggle_favorite(state, prompt_id)
            self._save_with_recovery(state)
            prompt = self._prompt_service.get_prompt(state, prompt_id)
            status = (
                "お気に入りに追加しました"
                if prompt.favorite
                else "お気に入りを削除しました"
            )
            logger.info(f"Favorite toggled: {prompt_id} -> {prompt.favorite}")
            if self._page:
                show_snackbar(self._page, status, bgcolor=SUCCESS_COLOR)
        except PromptNotFoundError as e:
            logger.error(f"Prompt not found on toggle favorite: {prompt_id}")
            if self._page:
                show_snackbar(self._page, str(e), bgcolor=ERROR_COLOR)
        except Exception as e:
            logger.error(f"Failed to toggle favorite for '{prompt_id}': {e}")
            if self._page:
                show_snackbar(
                    self._page, "お気に入りの更新に失敗しました", bgcolor=ERROR_COLOR
                )

    def on_category_change(self, state: AppState, category_id: Optional[str]) -> None:
        """カテゴリ選択を変更する。

        選択カテゴリを更新し、表示フィルタを適用。

        Args:
            state: 現在のアプリケーション状態。
            category_id: 選択するカテゴリ ID（None で全カテゴリ表示）。

        Returns:
            None
        """
        try:
            if category_id is not None:
                # 選択カテゴリの存在確認
                category = self._category_service.get_category(state, category_id)
                state.selected_category_id = category.id
            else:
                state.selected_category_id = None
            logger.info(f"Category selected: {category_id}")
        except CategoryNotFoundError as e:
            logger.error(f"Category not found on select: {category_id}")
            if self._page:
                show_snackbar(self._page, str(e), bgcolor=ERROR_COLOR)
        except Exception as e:
            logger.error(f"Failed to change category to '{category_id}': {e}")
            if self._page:
                show_snackbar(
                    self._page, "カテゴリ選択に失敗しました", bgcolor=ERROR_COLOR
                )

    def on_search(self, state: AppState, query: str) -> None:
        """検索クエリを更新し、検索サービスで結果を評価する。

        タイトルと本文を対象に部分一致検索を行う。UI 側では
        `get_filtered_prompts()` を介して結果が反映されるが、ここでは
        `SearchService` を用いて結果件数を評価・ログ記録する。

        Args:
            state: 現在のアプリケーション状態。
            query: 検索クエリ文字列。

        Returns:
            None

        Note:
            - Flet 0.28.3 API 準拠。
            - 検索 + （カテゴリ／お気に入り）複合フィルタは
              `get_filtered_prompts()` で最終適用される。
        """
        try:
            state.search_query = query

            # 事前に検索結果を評価（件数ログ）。実際の描画は呼び出し側で行う。
            base_prompts = self._prompt_service.list_active_prompts(state)
            category_path = self._resolve_selected_category_path(state)
            preview = self._search_service.apply_filters(
                base_prompts,
                query=query,
                category_path=category_path if category_path else None,
                favorite=False,
            )
            logger.info("Search updated: query='%s', matched=%d", query, len(preview))
        except Exception as e:
            logger.error(f"Failed to update search query: {e}")
            if self._page:
                show_snackbar(self._page, "検索に失敗しました", bgcolor=ERROR_COLOR)

    def get_filtered_prompts(
        self,
        state: AppState,
        include_favorite: bool = False,
    ) -> List[Prompt]:
        """フィルタ条件を適用したプロンプト一覧を取得。

        ゴミ箱除外、カテゴリフィルタ、検索クエリを適用。

        Args:
            state: 現在のアプリケーション状態。
            include_favorite: True の場合はお気に入りのみに絞る。

        Returns:
            フィルタ済みのプロンプト一覧。
        """
        try:
            # ゴミ箱内を除外
            prompts = self._prompt_service.list_active_prompts(state)

            # カテゴリ ID -> カテゴリ名のパス（前方一致用）へ解決
            category_path = self._resolve_selected_category_path(state)

            # 複合フィルタ適用（検索 + カテゴリ + お気に入り）
            result = self._search_service.apply_filters(
                prompts,
                query=state.search_query,
                category_path=category_path if category_path else None,
                favorite=include_favorite,
            )
            return result
        except Exception as e:
            logger.error(f"Failed to get filtered prompts: {e}")
            return []

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def _resolve_selected_category_path(self, state: AppState) -> List[str]:
        """選択カテゴリ ID を名称パス（ルートからの名前配列）へ解決する。

        `Prompt.category_path` は名称配列で保持しているため、
        前方一致フィルタに利用できるように選択カテゴリの名称パスを生成する。

        Args:
            state: 現在のアプリケーション状態。

        Returns:
            ルートから選択カテゴリまでの名称配列。未選択のときは空配列。
        """
        if not state.selected_category_id:
            return []
        path: List[str] = []
        current = state.get_category(state.selected_category_id)
        # 親を辿って名称を収集
        while current is not None:
            path.append(current.name)
            if current.parent_id is None:
                break
            current = state.get_category(current.parent_id)
        # ルート -> 選択 の順に並べ替え
        path.reverse()
        return path

    def _save_with_recovery(self, state: AppState) -> None:
        """状態保存を実行し、失敗時はバックアップ復元を試みる。

        Args:
            state: 保存対象のアプリケーション状態。

        Raises:
            DataPersistenceError: 保存および復元に失敗した場合。
        """
        try:
            self._data_service.save(state)
        except Exception as exc:
            logger.exception("Failed to persist state; attempting recovery")
            restored = False
            try:
                restored = self._data_service.restore_from_backup()
            except Exception:
                logger.exception("Restore from backup failed")

            if self._page:
                if restored:
                    show_snackbar(
                        self._page,
                        "保存に失敗しましたがバックアップから復元しました",
                        bgcolor=ERROR_COLOR,
                    )
                else:
                    show_snackbar(
                        self._page,
                        "保存に失敗しました。バックアップ復元も失敗しました",
                        bgcolor=ERROR_COLOR,
                    )
            # もとの例外を上位に伝搬（必要に応じて呼び出し側で処理）
            raise
