"""日時処理ユーティリティ。

Flet 0.28.3、Python 3.14.2 対応。
"""

from datetime import datetime
from typing import Optional


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """日時を指定フォーマットで文字列化。

    Args:
        dt: 日時オブジェクト。
        format_str: フォーマット文字列。

    Returns:
        フォーマット済み文字列。

    Example:
        >>> dt = datetime.now()
        >>> result = format_datetime(dt, "%Y-%m-%d")
        >>> len(result)
        10
    """
    return dt.strftime(format_str)


def format_datetime_relative(dt: datetime) -> str:
    """日時を相対表記でフォーマット。

    例：「2分前」「3時間前」

    Args:
        dt: 日時オブジェクト。

    Returns:
        相対表記の文字列。

    Example:
        >>> from datetime import timedelta
        >>> dt = datetime.now() - timedelta(minutes=5)
        >>> result = format_datetime_relative(dt)
        >>> "5分前" in result
        True
    """
    now = datetime.now()
    delta = now - dt

    seconds = delta.total_seconds()

    if seconds < 60:
        return "今"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes}分前"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours}時間前"
    elif seconds < 604800:
        days = int(seconds // 86400)
        return f"{days}日前"
    else:
        return format_datetime(dt, "%Y-%m-%d")


def is_today(dt: datetime) -> bool:
    """指定日時が今日か判定。

    Args:
        dt: 日時オブジェクト。

    Returns:
        今日の場合 True。

    Example:
        >>> from datetime import timedelta
        >>> dt = datetime.now()
        >>> is_today(dt)
        True
    """
    today = datetime.now().date()
    return dt.date() == today


def is_this_month(dt: datetime) -> bool:
    """指定日時が今月か判定。

    Args:
        dt: 日時オブジェクト。

    Returns:
        今月の場合 True。
    """
    now = datetime.now()
    return dt.year == now.year and dt.month == now.month
