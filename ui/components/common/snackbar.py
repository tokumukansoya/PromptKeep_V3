from __future__ import annotations

import flet as ft

from ui.styles.colors import SUCCESS_COLOR, ERROR_COLOR, BUTTON_BG
from ui.styles import spacing


def show_snackbar(
    page: ft.Page,
    message: str,
    duration_ms: int = 2000,
    bgcolor: str | None = None,
) -> None:
    """トースト通知（SnackBar）を表示する。

    右下寄せの控えめなスナックバーを表示し、指定時間後に自動で消えます。
    Flet 0.28.3 の `SnackBar` API を利用。

    Args:
        page: 表示対象の Flet ページ。
        message: 表示するメッセージ文字列。
        duration_ms: 表示時間（ミリ秒）。デフォルトは 2000ms。
        bgcolor: 背景色。未指定時は通常（控えめ）色を使用。
            - 成功メッセージには `SUCCESS_COLOR`
            - エラーメッセージには `ERROR_COLOR`
            - 通常はデフォルト背景色（`BUTTON_BG`）

    Returns:
        None

    Example:
        >>> # 通常メッセージ
        >>> show_snackbar(page, "コピーしました")
        >>> # 成功メッセージ
        >>> show_snackbar(page, "保存しました", bgcolor=SUCCESS_COLOR)
        >>> # エラーメッセージ
        >>> show_snackbar(page, "保存に失敗しました", bgcolor=ERROR_COLOR)
    """
    bg = bgcolor or BUTTON_BG

    # SnackBar をページに設定
    page.snack_bar = ft.SnackBar(  # type: ignore[attr-defined]
        content=ft.Text(message),
        bgcolor=bg,
        duration=duration_ms,
        behavior=ft.SnackBarBehavior.FLOATING,
        margin=ft.margin.only(right=spacing.MARGIN_MD, bottom=spacing.MARGIN_MD),
        # 右下寄せに近づけるための右/下マージン（控えめ）
        show_close_icon=False,
    )

    # 表示
    page.snack_bar.open = True  # type: ignore[attr-defined]
    page.update()
