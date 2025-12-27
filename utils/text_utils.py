"""テキスト処理ユーティリティ。

Flet 0.28.3、Python 3.14.2 対応。
"""

from config import PREVIEW_MAX_LENGTH


def truncate_preview(text: str, max_length: int = PREVIEW_MAX_LENGTH, suffix: str = "…") -> str:
    """テキストをプレビュー用に切り詰める。

    Args:
        text: 元のテキスト。
        max_length: 最大文字数。
        suffix: 省略記号。

    Returns:
        切り詰められたテキスト。

    Example:
        >>> text = "a" * 100
        >>> preview = truncate_preview(text)
        >>> len(preview) <= 83  # max + suffix
        True
    """
    if len(text) > max_length:
        return text[:max_length] + suffix
    return text


def truncate_title(text: str, max_length: int = 50) -> str:
    """タイトルを切り詰める。

    Args:
        text: 元のテキスト。
        max_length: 最大文字数。

    Returns:
        切り詰められたテキスト。
    """
    if len(text) > max_length:
        return text[:max_length] + "…"
    return text


def highlight_search_query(text: str, query: str, highlight_format: str = "**{text}**") -> str:
    """テキスト内の検索クエリをハイライト。

    Args:
        text: 元のテキスト。
        query: 検索クエリ。
        highlight_format: ハイライト形式。

    Returns:
        ハイライト済みテキスト。

    Example:
        >>> text = "Hello World"
        >>> result = highlight_search_query(text, "World")
        >>> "**World**" in result
        True
    """
    if not query:
        return text

    return text.replace(query, highlight_format.format(text=query))


def normalize_whitespace(text: str) -> str:
    """複数の空白を単一の空白に正規化。

    Args:
        text: 元のテキスト。

    Returns:
        正規化されたテキスト。

    Example:
        >>> text = "Hello  \\n  World"
        >>> result = normalize_whitespace(text)
        >>> result
        'Hello World'
    """
    return " ".join(text.split())


def is_empty_or_whitespace(text: str) -> bool:
    """テキストが空または空白のみか判定。

    Args:
        text: テキスト。

    Returns:
        空または空白のみの場合 True。

    Example:
        >>> is_empty_or_whitespace("  ")
        True
        >>> is_empty_or_whitespace("text")
        False
    """
    return not text or not text.strip()
