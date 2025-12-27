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

from config import LOG_LEVEL

# ログディレクトリの作成
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

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
logger.add(
    LOG_DIR / "promptkeep_{time:YYYY-MM-DD}.log",
    level=LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    rotation="1 day",
    retention="7 days",
    encoding="utf-8",
)

# モジュールからloggerをインポート可能にする
__all__ = ["logger"]
