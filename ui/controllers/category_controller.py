from __future__ import annotations

import logging
from typing import Optional

import flet as ft

from models.app_state import AppState
from services.category_service import CategoryService
from services.data_service import DataService
from exceptions import InvalidCategoryDepthError, CategoryNotFoundError
from ui.components.common.snackbar import show_snackbar
from ui.styles.colors import ERROR_COLOR

logger = logging.getLogger(__name__)


class CategoryController:
    """カテゴリ操作のコントローラー。

    カテゴリの追加・移動・削除・選択といった操作を仲介し、
    サービス呼び出しと永続化を行う。エラー時はスナックバーで通知する。

    Args:
        category_service: カテゴリの CRUD / 移動を提供するサービス。
        data_service: データ永続化を担当するサービス。
    """

    def __init__(
        self, category_service: CategoryService, data_service: DataService
    ) -> None:
        """CategoryController の初期化。"""
        self._category_service = category_service
        self._data_service = data_service
        self._page: Optional[ft.Page] = None
        logger.debug("CategoryController initialized")

    def attach_page(self, page: ft.Page) -> None:
        """Snackbar 表示用に Flet `Page` を関連付ける。"""
        self._page = page

    def on_add_category(
        self, state: AppState, name: str, parent_id: Optional[str]
    ) -> None:
        """カテゴリを追加する。

        兄弟末尾に追加し、成功後に状態を保存する。

        Args:
            state: 現在のアプリケーション状態。
            name: 追加するカテゴリ名。
            parent_id: 親カテゴリ ID。ルート追加時は `None`。
        """
        try:
            self._category_service.create_category(
                state, name=name, parent_id=parent_id
            )
            self._data_service.save(state)
            logger.info("Category added: name=%s parent=%s", name, parent_id)
        except InvalidCategoryDepthError as e:
            logger.error("Invalid category depth on add: %s", e)
            if self._page:
                show_snackbar(self._page, str(e), bgcolor=ERROR_COLOR)
        except CategoryNotFoundError as e:
            logger.error("Parent category not found on add: %s", e)
            if self._page:
                show_snackbar(self._page, str(e), bgcolor=ERROR_COLOR)
        except Exception as e:
            logger.error("Failed to add category '%s': %s", name, e)
            if self._page:
                show_snackbar(
                    self._page, "カテゴリの追加に失敗しました", bgcolor=ERROR_COLOR
                )

    def on_move_category(
        self, state: AppState, category_id: str, new_parent_id: Optional[str]
    ) -> None:
        """カテゴリを別の親配下へ移動する。

        深さ制約や循環参照に違反した場合はエラーを通知する。

        Args:
            state: 現在のアプリケーション状態。
            category_id: 移動対象カテゴリ ID。
            new_parent_id: 新しい親カテゴリ ID。ルート移動時は `None`。
        """
        try:
            self._category_service.move_category(
                state, category_id=category_id, new_parent_id=new_parent_id
            )
            self._data_service.save(state)
            logger.info(
                "Category moved: id=%s new_parent=%s", category_id, new_parent_id
            )
        except InvalidCategoryDepthError as e:
            logger.error("Invalid category depth on move: %s", e)
            if self._page:
                show_snackbar(self._page, str(e), bgcolor=ERROR_COLOR)
        except CategoryNotFoundError as e:
            logger.error("Category or parent not found on move: %s", e)
            if self._page:
                show_snackbar(self._page, str(e), bgcolor=ERROR_COLOR)
        except Exception as e:
            logger.error("Failed to move category '%s': %s", category_id, e)
            if self._page:
                show_snackbar(
                    self._page, "カテゴリの移動に失敗しました", bgcolor=ERROR_COLOR
                )

    def on_delete_category(self, state: AppState, category_id: str) -> None:
        """カテゴリを削除する（配下のサブツリーも削除）。

        Args:
            state: 現在のアプリケーション状態。
            category_id: 削除対象カテゴリ ID。
        """
        try:
            self._category_service.delete_category(state, category_id=category_id)
            self._data_service.save(state)
            logger.info("Category deleted: id=%s", category_id)
        except CategoryNotFoundError as e:
            logger.error("Category not found on delete: %s", e)
            if self._page:
                show_snackbar(self._page, str(e), bgcolor=ERROR_COLOR)
        except Exception as e:
            logger.error("Failed to delete category '%s': %s", category_id, e)
            if self._page:
                show_snackbar(
                    self._page, "カテゴリの削除に失敗しました", bgcolor=ERROR_COLOR
                )

    def on_select_category(self, state: AppState, category_id: str) -> None:
        """カテゴリ選択を更新する。

        選択状態を保存し、必要に応じて永続化する。

        Args:
            state: 現在のアプリケーション状態。
            category_id: 選択するカテゴリ ID。
        """
        try:
            state.selected_category_id = category_id
            self._data_service.save(state)
            logger.info("Category selected: id=%s", category_id)
        except Exception as e:
            logger.error("Failed to select category '%s': %s", category_id, e)
            if self._page:
                show_snackbar(
                    self._page, "カテゴリ選択に失敗しました", bgcolor=ERROR_COLOR
                )
