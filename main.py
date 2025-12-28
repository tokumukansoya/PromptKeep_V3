"""Flet アプリケーションのメインエントリーポイント。

PromptKeep アプリケーション。
Flet 0.28.3、Python 3.14.2 対応。

このファイルはアプリケーションを起動する。
"""

import sys
from importlib.metadata import PackageNotFoundError, version

# バージョン確認
from config import (
    MIN_PYTHON_VERSION,
    REQUIRED_FLET_VERSION,
)

# Loguru ロガー（自動設定済み）
from utils.logger import logger


def check_versions() -> None:
    """必須バージョンをチェック。

    Raises:
        SystemExit: バージョンが適切でない場合。
    """
    # Python バージョン確認
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    logger.info(f"Python version: {python_version} (required: {MIN_PYTHON_VERSION}+")

    if sys.version_info < (3, 12, 3):
        logger.error(f"Python 3.12.3+ required, got {python_version}")
        raise SystemExit(f"Python 3.12.3以上が必要です（現在: {python_version}）")

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

    logger.info("PromptKeep Application initialized")
    logger.info("UI implementation pending...")
    print("\n✓ PromptKeep is ready for UI implementation!")
    print("✓ Current status: Data layer and services are ready.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
        sys.exit(1)