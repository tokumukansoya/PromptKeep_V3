"""カスタム例外クラス。

PromptKeep 独自の例外定義。
Flet 0.28.3、Python 3.14.2 対応。
"""


class PromptKeeperError(Exception):
    """PromptKeep 全体の基底例外。"""

    pass


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

    pass


class DataPersistenceError(PromptKeeperError):
    """データ永続化に失敗した場合の例外。

    JSON の読み込み・書き込み失敗時に発生。
    """

    pass


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
