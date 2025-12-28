"""ロギング設定 - Loguru を使用した統一ロギング。

Flet 0.28.3、Python 3.14.2 対応。

Example:
    >>> from utils.logger import logger
    >>> logger.info("アプリケーション開始")
    >>> logger.error("エラーが発生しました")
"""

import sys
from pathlib import Path

from loguru import logger

# ログディレクトリの作成（PyInstaller対応）
from utils.path_utils import get_log_dir

LOG_DIR = get_log_dir()
try:
    LOG_DIR.mkdir(exist_ok=True, parents=True)
except OSError:
    # ディレクトリ作成に失敗した場合はカレントディレクトリを使用
    LOG_DIR = Path(".")

# config.pyはloggerをインポートするため、循環インポートを避けてデフォルト値を使用
LOG_LEVEL = "INFO"

# デフォルトのシンクを削除（重複防止）
logger.remove()

# コンソール出力（カラフル）
logger.add(
    sys.stderr,
    level=LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>",
    colorize=True,
)

# ファイル出力（日次ローテーション）
try:
    logger.add(
        LOG_DIR / "promptkeep_{time:YYYY-MM-DD}.log",
        level=LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        rotation="1 day",
        retention="7 days",
        encoding="utf-8",
    )
except Exception:
    # ファイル出力の設定に失敗した場合はスキップ（コンソール出力のみ）
    pass

# モジュールからloggerをインポート可能にする
__all__ = ["logger"]
