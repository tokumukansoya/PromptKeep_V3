"""アンドゥサービス。

直前の削除操作などを 1 ステップだけ戻すための状態スタックを提供。
Flet 0.28.3、Python 3.14.2 対応。

Note:
    - 本サービスは `AppState` のスナップショット（`dict`）を保持する。
    - 実際の状態復元（`AppState.from_dict(...)` での適用）や永続化は
      呼び出し側で実施する。
"""

import logging
from typing import List, Optional, Dict

from models.app_state import AppState

logger = logging.getLogger(__name__)


class UndoService:
    """直前状態のアンドゥ管理を提供するサービス。

    Attributes:
        max_stack_size: 保持するスナップショットの最大数（既定: 1）。
        _stack: AppState スナップショット（dict）のスタック。
    """

    def __init__(self, max_stack_size: int = 1) -> None:
        """UndoService の初期化。

        Args:
            max_stack_size: 保持するスナップショットの最大数。
                             Phase2 では 1 を前提（直前のみ）。
        """
        if max_stack_size < 1:
            logger.error("max_stack_size must be >= 1")
            max_stack_size = 1

        self.max_stack_size: int = max_stack_size
        self._stack: List[Dict] = []
        logger.debug("UndoService initialized (max_stack_size=%s)", max_stack_size)

    def push_state(self, state: AppState) -> None:
        """現在の状態をスナップショットとしてスタックに積む。

        削除操作直前など、元に戻せるように呼び出し側で実行する。

        Args:
            state: 現在のアプリケーション状態。
        """
        try:
            snapshot = state.to_dict()
            self._stack.append(snapshot)
            # 余剰分を削る（直前のみ保持）
            if len(self._stack) > self.max_stack_size:
                self._stack = self._stack[-self.max_stack_size :]
            logger.info("Pushed state snapshot (stack_size=%s)", len(self._stack))
        except Exception as exc:
            logger.exception("Failed to push state snapshot")
            raise RuntimeError(
                f"アンドゥ用スナップショットの保存に失敗しました: {exc}"
            ) from exc

    def can_undo(self) -> bool:
        """アンドゥ可能かどうかを返す。

        Returns:
            スタックが空でなければ True。
        """
        return len(self._stack) > 0

    def undo(self) -> Optional[dict]:
        """直前の状態スナップショットを取り出して返す。

        Returns:
            スナップショット（dict）を返す。スタックが空の場合は None。
        """
        if not self._stack:
            logger.error("Undo requested but stack is empty")
            return None
        try:
            snapshot = self._stack.pop()
            logger.info("Undo performed (remaining_stack=%s)", len(self._stack))
            return snapshot
        except Exception as exc:
            logger.exception("Failed to pop undo snapshot")
            raise RuntimeError(f"アンドゥ処理に失敗しました: {exc}") from exc

    def clear(self) -> None:
        """スタックをクリアする。"""
        try:
            self._stack.clear()
            logger.info("Undo stack cleared")
        except Exception as exc:
            logger.exception("Failed to clear undo stack")
            raise RuntimeError(
                f"アンドゥスタックのクリアに失敗しました: {exc}"
            ) from exc
