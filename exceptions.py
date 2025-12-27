"""カスタム例外クラス。

PromptKeep 独自の例外定義。
Flet 0.28.3、Python 3.14.2 対応。
"""


class PromptKeeperError(Exception):
    """PromptKeep 全体の基底例外。

    Attributes:
        message: 開発者向けエラーメッセージ
        user_message: ユーザー向け表示メッセージ（UI通知用）
    """

    def __init__(self, message: str, user_message: str | None = None):
        """例外を初期化。

        Args:
            message: 開発者向けエラーメッセージ（ログ記録用）
            user_message: ユーザー向けメッセージ（省略時はmessageを使用）
        """
        self.message = message
        self.user_message = user_message or message
        super().__init__(message)


class PromptNotFoundError(PromptKeeperError):
    """プロンプトが見つからない場合の例外。"""

    pass


class CategoryNotFoundError(PromptKeeperError):
    """カテゴリが見つからない場合の例外。"""

    pass


class InvalidCategoryDepthError(PromptKeeperError):
    """カテゴリの階層が深すぎる場合の例外。

    config.MAX_CATEGORY_DEPTH を超える場合に発生。
    """

    def __init__(self, current_depth: int, max_depth: int = 3):
        super().__init__(
            f"Category depth {current_depth} exceeds maximum {max_depth}",
            user_message=f"カテゴリは最大{max_depth}階層までです",
        )
        self.current_depth = current_depth
        self.max_depth = max_depth


class DataPersistenceError(PromptKeeperError):
    """データ永続化に失敗した場合の例外。

    JSON の読み込み・書き込み失敗時に発生。
    """

    def __init__(self, operation: str, reason: str):
        super().__init__(
            f"Data persistence failed during {operation}: {reason}",
            user_message="データの保存に失敗しました。変更が失われる可能性があります。",
        )
        self.operation = operation
        self.reason = reason


class InvalidDataError(PromptKeeperError):
    """不正なデータ形式の例外。

    JSON スキーマ不適合やデータ型エラー時に発生。
    """

    pass


class ValidationError(PromptKeeperError):
    """データバリデーション失敗の例外。

    ビジネスロジックの制約に違反する場合に発生。
    """

    pass
