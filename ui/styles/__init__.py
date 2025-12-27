"""UI スタイルパッケージの初期化。

ダークテーマ用のカラー、フォント、余白定義を提供。
"""

from ui.styles.colors import *
from ui.styles.spacing import *
from ui.styles.typography import *

__all__ = [
    "DARK_BG",
    "DARK_BG_SECONDARY",
    "DARK_BG_TERTIARY",
    "TEXT_PRIMARY",
    "TEXT_SECONDARY",
    "TEXT_DISABLED",
    "ACCENT_COLOR",
    "SUCCESS_COLOR",
    "ERROR_COLOR",
    "WARNING_COLOR",
    "BUTTON_BG",
    "BUTTON_BG_HOVER",
    "FONT_FAMILY",
    "FONT_SIZE_BODY",
    "FONT_SIZE_TITLE",
    "FONT_SIZE_CAPTION",
    "PADDING_XS",
    "PADDING_SM",
    "PADDING_MD",
    "PADDING_LG",
]
