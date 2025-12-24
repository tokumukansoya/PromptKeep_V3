"""データ永続化サービス。

JSON ファイルの読み書きを担当。
Flet 0.28.3、Python 3.14.2 対応。
"""

import json
import logging
from typing import Optional
from pathlib import Path

from config import DATA_DIR, PROMPTS_FILE, BACKUP_DIR
from models.app_state import AppState
from exceptions import DataPersistenceError, InvalidDataError

logger = logging.getLogger(__name__)


class DataService:
    """データ永続化を担当するサービス。

    JSON ファイルの読み込み・書き込み、バックアップを管理。

    Attributes:
        data_dir: データディレクトリパス。
        prompts_file: プロンプトファイルパス。
        backup_dir: バックアップディレクトリパス。

    Note:
        - 初期化時に必要なディレクトリを自動作成。
        - 書き込み失敗時はロールバック機能を提供。
    """

    def __init__(
        self,
        data_dir: str = DATA_DIR,
        prompts_file: str = PROMPTS_FILE,
        backup_dir: str = BACKUP_DIR,
    ) -> None:
        """DataService の初期化。

        Args:
            data_dir: データディレクトリパス。
            prompts_file: プロンプトファイルパス。
            backup_dir: バックアップディレクトリパス。
        """
        self.data_dir = Path(data_dir)
        self.prompts_file = Path(prompts_file)
        self.backup_dir = Path(backup_dir)

        self._ensure_directories_exist()
        logger.debug(f"DataService initialized: {self.prompts_file}")

    def _ensure_directories_exist(self) -> None:
        """必要なディレクトリを作成。

        Raises:
            DataPersistenceError: ディレクトリ作成に失敗した場合。
        """
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directories ensured: {self.data_dir}, {self.backup_dir}")
        except OSError as e:
            logger.error(f"Failed to create directories: {e}")
            raise DataPersistenceError(f"ディレクトリ作成に失敗しました: {e}")

    def load(self) -> AppState:
        """AppState をファイルから読み込む。

        ファイルが存在しない場合は空の AppState を返す。

        Returns:
            読み込んだ AppState オブジェクト。

        Raises:
            DataPersistenceError: ファイル読み込みに失敗した場合。
            InvalidDataError: データ形式が不正な場合。

        Example:
            >>> service = DataService()
            >>> state = service.load()
            >>> print(len(state.prompts))
            0
        """
        try:
            if not self.prompts_file.exists():
                logger.info(
                    f"Prompts file not found, returning empty state: {self.prompts_file}"
                )
                return AppState.empty()

            with open(self.prompts_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            state = AppState.from_dict(data)
            logger.info(
                f"Loaded {len(state.prompts)} prompts and {len(state.categories)} categories"
            )
            return state

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise InvalidDataError(f"JSON の形式が不正です: {e}")
        except IOError as e:
            logger.error(f"File read error: {e}")
            raise DataPersistenceError(f"ファイル読み込みに失敗しました: {e}")
        except (ValueError, TypeError) as e:
            logger.error(f"Data validation error: {e}")
            raise InvalidDataError(f"データ形式が不正です: {e}")

    def save(self, state: AppState) -> None:
        """AppState をファイルに保存。

        書き込み失敗時はバックアップから復元。

        Args:
            state: 保存する AppState オブジェクト。

        Raises:
            DataPersistenceError: ファイル書き込みに失敗した場合。

        Example:
            >>> service = DataService()
            >>> state = AppState.empty()
            >>> service.save(state)
        """
        temp_file = self.prompts_file.with_suffix(".tmp")

        try:
            # 既存ファイルがあればバックアップ
            if self.prompts_file.exists():
                self.create_backup()

            # テンポラリファイルに書き込み
            with open(temp_file, "w", encoding="utf-8") as f:
                data = state.to_dict()
                json.dump(data, f, indent=2, ensure_ascii=False)

            # テンポラリファイルを本ファイルに置き換え
            temp_file.replace(self.prompts_file)
            logger.info(
                f"Saved {len(state.prompts)} prompts and {len(state.categories)} categories"
            )

        except IOError as e:
            logger.error(f"File write error: {e}")
            if temp_file.exists():
                temp_file.unlink()
            raise DataPersistenceError(f"ファイル保存に失敗しました: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during save: {e}")
            if temp_file.exists():
                temp_file.unlink()
            raise DataPersistenceError(f"予期しないエラーが発生しました: {e}")

    def create_backup(self) -> None:
        """現在のプロンプトファイルをバックアップ。

        Raises:
            DataPersistenceError: バックアップ作成に失敗した場合。
        """
        try:
            if not self.prompts_file.exists():
                return

            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"prompts_backup_{timestamp}.json"

            with open(self.prompts_file, "r", encoding="utf-8") as src:
                with open(backup_file, "w", encoding="utf-8") as dst:
                    dst.write(src.read())

            logger.debug(f"Backup created: {backup_file}")

        except IOError as e:
            logger.warning(f"Failed to create backup: {e}")

    def restore_from_backup(self, backup_file: Optional[str] = None) -> bool:
        """バックアップからデータを復元。

        Args:
            backup_file: 復元するバックアップファイルパス。
                        未指定時は最新のバックアップを使用。

        Returns:
            復元に成功した場合 True、失敗した場合 False。
        """
        try:
            if backup_file is None:
                # 最新のバックアップを探す
                backups = sorted(
                    self.backup_dir.glob("prompts_backup_*.json"), reverse=True
                )
                if not backups:
                    logger.warning("No backup files found")
                    return False
                backup_file = str(backups[0])

            backup_path = Path(backup_file)
            if not backup_path.exists():
                logger.error(f"Backup file not found: {backup_path}")
                return False

            with open(backup_path, "r", encoding="utf-8") as src:
                with open(self.prompts_file, "w", encoding="utf-8") as dst:
                    dst.write(src.read())

            logger.info(f"Restored from backup: {backup_path}")
            return True

        except IOError as e:
            logger.error(f"Failed to restore from backup: {e}")
            return False
