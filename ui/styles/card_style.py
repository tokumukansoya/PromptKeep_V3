"""カードスタイル定義。

Flet 0.28.3、Python 3.14.2 対応。
プロンプトカードの視覚的定義を一元管理。
"""

from config import MAX_CATEGORY_DEPTH
from ui.styles.colors import BORDER_COLOR, DARK_BG_SECONDARY, TEXT_PRIMARY
from ui.styles.spacing import BORDER_RADIUS_MD, PADDING_MD

# ============================================================================
# カード全体
# ============================================================================
CARD_WIDTH = 200  # 正方形カード
CARD_HEIGHT = 200  # 正方形カード
CARD_BG_COLOR = DARK_BG_SECONDARY
CARD_BORDER_COLOR = BORDER_COLOR
CARD_BORDER_WIDTH = 1
CARD_BORDER_RADIUS = BORDER_RADIUS_MD

# ============================================================================
# カードコンテンツパディング
# ============================================================================
CARD_PADDING = PADDING_MD

# ============================================================================
# カードテキスト
# ============================================================================
CARD_TITLE_COLOR = TEXT_PRIMARY
CARD_PREVIEW_COLOR = TEXT_PRIMARY

# ============================================================================
# ホバー・インタラクション
# ============================================================================
CARD_HOVER_OPACITY = 0.8
CARD_ACTIVE_OPACITY = 0.6