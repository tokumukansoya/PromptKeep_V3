"""パスユーティリティ - PyInstaller対応。

exe化した際に正しいパスを解決するためのユーティリティ。
"""

import sys
from pathlib import Path


def get_app_dir() -> Path:
    """アプリケーションのベースディレクトリを取得する。
    
    PyInstallerでexe化された場合は実行ファイルのディレクトリ、
    通常のPython実行時はスクリプトのディレクトリを返す。
    
    Returns:
        アプリケーションのベースディレクトリ
    """
    if getattr(sys, 'frozen', False):
        # PyInstallerでexe化されている場合
        # sys.executable はexeファイルのパス
        return Path(sys.executable).parent
    else:
        # 通常のPython実行
        # main.pyがあるディレクトリを返す
        return Path(__file__).parent.parent


def get_data_dir() -> Path:
    """データディレクトリのパスを取得する。
    
    Returns:
        データディレクトリのパス
    """
    return get_app_dir() / "data"


def get_prompts_file() -> Path:
    """プロンプトファイルのパスを取得する。
    
    Returns:
        プロンプトファイルのパス
    """
    return get_data_dir() / "prompts.json"


def get_backup_dir() -> Path:
    """バックアップディレクトリのパスを取得する。
    
    Returns:
        バックアップディレクトリのパス
    """
    return get_data_dir() / "backup"


def get_log_dir() -> Path:
    """ログディレクトリのパスを取得する。
    
    Returns:
        ログディレクトリのパス
    """
    return get_app_dir() / "logs"


def get_asset_path(asset_name: str) -> Path:
    """アセットファイルのパスを取得する。
    
    PyInstallerでバンドルされたアセットにも対応。
    
    Args:
        asset_name: アセットファイル名（例: "icon.png"）
    
    Returns:
        アセットファイルのパス
    """
    if getattr(sys, 'frozen', False):
        # PyInstallerでexe化されている場合
        # _MEIPASS は一時展開ディレクトリ
        base_path = Path(getattr(sys, '_MEIPASS', Path(sys.executable).parent))
    else:
        base_path = get_app_dir()
    
    return base_path / "assets" / asset_name
