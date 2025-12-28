# アプリケーション設定定数

# ログレベル設定
LOG_LEVEL = "INFO"

# Pythonの最小バージョン
MIN_PYTHON_VERSION = (3, 8)

# カテゴリの最大深度
MAX_CATEGORY_DEPTH = 3

# 必須のFletバージョン
REQUIRED_FLET_VERSION = "0.80.0"

# データパス設定（PyInstaller対応）
# 実際のパスはutils.path_utilsを使用して解決する
# これらはデフォルト値として残す（互換性のため）
from utils.path_utils import get_data_dir, get_prompts_file, get_backup_dir

DATA_DIR = str(get_data_dir())
PROMPTS_FILE = str(get_prompts_file())
BACKUP_DIR = str(get_backup_dir())

# プレビュー設定
PREVIEW_MAX_LENGTH = 80
PREVIEW_MIN_LENGTH = 40

# 自動保存設定
DEBOUNCE_SECONDS = 2.0