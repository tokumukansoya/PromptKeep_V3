"""Flet アプリケーションのメインエントリーポイント。

PromptKeep アプリケーション。
Flet 0.28.3、Python 3.14.2 対応。

このファイルはアプリケーションを起動する。
"""

import sys
import logging
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError

# バージョン確認
import flet as ft
from config import (
    REQUIRED_FLET_VERSION,
    MIN_PYTHON_VERSION,
    LOG_LEVEL,
    LOG_FORMAT,
)

# ログ設定
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
)
logger = logging.getLogger(__name__)


def check_versions() -> None:
    """必須バージョンをチェック。

    Raises:
        SystemExit: バージョンが適切でない場合。
    """
    # Python バージョン確認
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    logger.info(f"Python version: {python_version} (required: {MIN_PYTHON_VERSION}+)")

    if sys.version_info < (3, 14):
        logger.error(f"Python 3.14+ required, got {python_version}")
        raise SystemExit(f"Python 3.14以上が必要です（現在: {python_version}）")

    # Flet バージョン確認
    try:
        flet_version = version("flet")
    except PackageNotFoundError:
        flet_version = "unknown"

    logger.info(f"Flet version: {flet_version} (required: {REQUIRED_FLET_VERSION})")

    if flet_version != REQUIRED_FLET_VERSION:
        logger.warning(
            f"Flet version mismatch: expected {REQUIRED_FLET_VERSION}, got {flet_version}"
        )


def main() -> None:
    """メインアプリケーション。

    エントリーポイント。
    """
    logger.info("=" * 70)
    logger.info("PromptKeep Application Starting")
    logger.info("=" * 70)

    # バージョン確認
    check_versions()

    # ここから UI 層のインポートと初期化
    logger.info("Initializing application...")

    from ui.app import PromptKeepApp

    app = PromptKeepApp()
    app.run()

    logger.info("PromptKeep Application terminated normally")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
        sys.exit(1)
