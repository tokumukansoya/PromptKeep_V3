# PromptKeep コーディング規約

## 環境・バージョン（厳守）

- **Python**: 3.14.2 以上（プロジェクトでは 3.14.2 を使用）
- **Flet**: 0.28.3（AIにこのバージョン以外を使わせない）
- **その他主要パッケージ**: 詳細は `requirements.txt` 参照

**重要**: AIに指示する際は、必ずバージョン番号を明示してください。例：
```
「Flet 0.28.3を使ってください」
「Python 3.14.2の機能を使ってください」
```

---

## 1. ファイル構成

### 1.1 ファイルヘッダー
すべての Python ファイルの先頭に以下を記載：

```python
"""モジュールの簡潔な説明（1行）

より詳しい説明が必要な場合は、ここに複数行で記述。
例：このモジュールはプロンプトのCRUD操作を提供する。

Attributes:
    CONSTANT_NAME: 説明

Note:
    Flet 0.28.3 との互換性を考慮して実装している。
"""

import ...
```

### 1.2 インポート順序
```python
# 1. 標準ライブラリ
import json
import logging
from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime

# 2. サードパーティライブラリ
import flet as ft

# 3. ローカルモジュール
from models.prompt import Prompt
from services.data_service import DataService
from ui.styles.colors import DARK_BG
```

**ルール**:
- 各セクション間に空行を1つ
- 同じセクション内ではアルファベット順
- `from X import Y` と `import X` は混在してもOK

### 1.3 ファイル行数
制限なし。ただし 500 行を超える場合は分割を検討。

---

## 2. 型ヒント（必須・厳格化）

### 2.1 関数の型定義
**すべての関数に型ヒントを付ける**（引数と戻り値）

```python
def create_prompt(
    title: str,
    body: str,
    category_ids: List[str]
) -> Prompt:
    """プロンプトを新規作成する。
    
    Args:
        title: プロンプトのタイトル。
        body: プロンプトの本文。
        category_ids: カテゴリIDの階層（IDベース）。
        body: プロンプトの本文。
        category_ids: カテゴリID階層（IDベース）。
    
    Returns:
        新しく作成された Prompt オブジェクト。
    """
    pass
```

### 2.2 複雑な型ヒント
`Optional`, `Union`, `Dict` などは必ず明記：

```python
from typing import Optional, Union, Dict, List, Tuple, Callable

# 良い例
def get_prompt(
    prompt_id: str
) -> Optional[Prompt]:
    ...

def filter_prompts(
    category: Optional[str] = None,
    favorite: bool = False
) -> List[Prompt]:
    ...

def save_data(
    data: Dict[str, List[Dict]]
) -> Union[bool, Exception]:
    ...

# コールバック型
def on_complete(callback: Callable[[Prompt], None]) -> None:
    ...
```

### 2.3 クラス属性の型定義
```python
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Prompt:
    """プロンプト model."""
    id: str
    title: str
    body: str
    category_ids: List[str]  # IDベース
    favorite: bool
    deleted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
```

### 2.4 型チェック用ツール（推奨）
- `mypy` でスタティック型チェック
- AIに指示する際：「mypy でチェック可能なコードを書いてください」

---

## 3. Docstring（Google Style 必須）

### 3.1 関数/メソッドの Docstring

```python
def update_prompt(
    prompt_id: str,
    title: Optional[str] = None,
    body: Optional[str] = None,
    favorite: Optional[bool] = None
) -> Prompt:
    """既存プロンプトを更新する。
    
    指定された属性のみ更新。未指定の属性は変更しない。
    
    Args:
        prompt_id: 更新対象のプロンプト ID。
        title: 新しいタイトル（省略時は変更しない）。
        body: 新しい本文（省略時は変更しない）。
        favorite: お気に入り状態（省略時は変更しない）。
    
    Returns:
        更新後の Prompt オブジェクト。
    
    Raises:
        ValueError: prompt_id が見つからない場合。
        TypeError: 引数の型が不正な場合。
    
    Example:
        >>> prompt = update_prompt("id123", title="新しいタイトル")
        >>> print(prompt.title)
        新しいタイトル
    """
    pass
```

### 3.2 クラスの Docstring

```python
class PromptService:
    """プロンプトの CRUD 操作を提供するサービス。
    
    DataService を通じてデータを永続化。
    
    Attributes:
        data_service: データ永続化を担当するサービス。
        prompts: メモリ上に保持するプロンプト一覧。
    
    Note:
        Flet 0.28.3 との互換性を確保しています。
    """
    pass
```

### 3.3 モジュール Docstring
ファイルの最初に記載（前述の「1.1 ファイルヘッダー」を参照）

---

## 4. エラーハンドリング

### 4.1 ロギング設定
```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 開発時は DEBUG

handler = logging.StreamHandler()  # コンソール出力
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
```

### 4.2 エラーログの出力（開発中はコンソールのみ）
```python
try:
    prompt = get_prompt(prompt_id)
except ValueError as e:
    logger.error(f"プロンプト取得失敗: {e}")
    raise

try:
    save_data(data)
except IOError as e:
    logger.exception("データ保存中にエラーが発生しました")
    raise
```

### 4.3 カスタム例外クラス
```python
# exceptions.py に定義

class PromptNotFoundError(Exception):
    """プロンプトが見つからない場合の例外。"""
    pass

class InvalidCategoryDepthError(Exception):
    """カテゴリの階層が深すぎる場合の例外。"""
    pass

class DataPersistenceError(Exception):
    """データ永続化に失敗した場合の例外。"""
    pass
```

**使用例**:
```python
def get_prompt(prompt_id: str) -> Prompt:
    """..."""
    if prompt not in self.prompts:
        logger.error(f"プロンプト {prompt_id} が見つかりません")
        raise PromptNotFoundError(f"ID: {prompt_id}")
```

---

## 5. 定数管理

### 5.1 定数の配置
- **色**: `ui/styles/colors.py`
- **フォント**: `ui/styles/typography.py`
- **余白/サイズ**: `ui/styles/spacing.py`
- **アプリ設定**: `config.py`（ルートディレクトリ）

### 5.2 config.py の例
```python
"""アプリケーション設定定数。

Flet 0.28.3、Python 3.14.2 環境での実行を想定。
"""

# バージョン
APP_VERSION = "1.0.0"
MIN_PYTHON_VERSION = "3.14.2"
REQUIRED_FLET_VERSION = "0.28.3"

# データ
DATA_DIR = "data"
PROMPTS_FILE = "data/prompts.json"
BACKUP_DIR = "data/backup"

# UI
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CARD_SIZE = 200  # 正方形カードのサイズ
PREVIEW_MAX_LENGTH = 80  # 本文プレビューの最大文字数

# カテゴリ
MAX_CATEGORY_DEPTH = 3
MAX_CATEGORY_NAME_LENGTH = 50

# ゴミ箱
TRASH_MAX_ITEMS = None  # None = 無期限

# デバウンス
AUTOSAVE_DEBOUNCE_MS = 2000
```

### 5.3 styles/colors.py の例
```python
"""ダークテーマ用カラーパレット。

Flet 0.28.3 での使用を想定。
"""

# 背景色
DARK_BG = "#1e1e1e"
DARK_BG_SECONDARY = "#2d2d2d"
DARK_BG_TERTIARY = "#3d3d3d"

# テキスト色
TEXT_PRIMARY = "#e0e0e0"
TEXT_SECONDARY = "#b0b0b0"
TEXT_DISABLED = "#808080"

# アクセント
ACCENT_COLOR = "#4a9eff"
SUCCESS_COLOR = "#4caf50"
ERROR_COLOR = "#f44336"
WARNING_COLOR = "#ff9800"

# ボタン
BUTTON_BG = "#404040"
BUTTON_BG_HOVER = "#505050"
```

### 5.4 定数の使用
```python
from config import PREVIEW_MAX_LENGTH, MAX_CATEGORY_DEPTH
from ui.styles.colors import DARK_BG, TEXT_PRIMARY

def truncate_preview(text: str) -> str:
    """テキストをプレビュー用に切り詰める。"""
    if len(text) > PREVIEW_MAX_LENGTH:
        return text[:PREVIEW_MAX_LENGTH] + "…"
    return text

def validate_category_depth(path: List[str]) -> bool:
    """カテゴリの階層が有効か確認する。"""
    return len(path) <= MAX_CATEGORY_DEPTH
```

---

## 6. コメント密度

### 6.1 ルール
- **Docstring は必須**：すべての公開関数/クラスに記載
- **複雑なロジック内のコメント**：必要に応じて記載
- **明白な処理**：コメント不要

### 6.2 良い例と悪い例

**良い例**（Docstring が充実、内部コメント不要）:
```python
def delete_prompt(self, prompt_id: str) -> None:
    """プロンプトをゴミ箱に移動する。
    
    Args:
        prompt_id: 削除対象のプロンプト ID。
    
    Raises:
        PromptNotFoundError: プロンプトが見つからない場合。
    """
    prompt = self._find_prompt(prompt_id)
    if not prompt:
        raise PromptNotFoundError(f"ID: {prompt_id}")
    
    prompt.deleted_at = datetime.now()
    self.trash.append(prompt_id)
    self._auto_save()
```

**良い例**（複雑なロジックにコメント追加）:
```python
def build_category_tree(
    categories: List[Category]
) -> Dict[str, List[Category]]:
    """カテゴリをツリー構造に変換する。
    
    Args:
        categories: フラットなカテゴリリスト。
    
    Returns:
        親 ID をキーとした子カテゴリのマッピング。
    """
    tree: Dict[str, List[Category]] = {}
    
    # parent_id ごとにグループ化
    for category in categories:
        parent_id = category.parent_id or "root"
        if parent_id not in tree:
            tree[parent_id] = []
        tree[parent_id].append(category)
    
    return tree
```

**悪い例**（過度なコメント）:
```python
# プロンプトを削除する
def delete_prompt(self, prompt_id: str) -> None:
    # プロンプトを探す
    prompt = self._find_prompt(prompt_id)
    # 見つかったか確認する
    if not prompt:
        # 見つからなかったら例外を発生させる
        raise PromptNotFoundError(f"ID: {prompt_id}")
    # 削除時刻を設定する
    prompt.deleted_at = datetime.now()
    # ゴミ箱に追加する
    self.trash.append(prompt_id)
    # 自動保存する
    self._auto_save()
```

---

## 7. 命名規則

### 7.1 PEP 8 に準拠

| 対象 | ルール | 例 |
|------|--------|-----|
| 関数/メソッド | snake_case | `get_prompt`, `on_delete_button_click` |
| 変数 | snake_case | `prompt_list`, `is_favorite` |
| 定数 | UPPER_SNAKE_CASE | `MAX_CATEGORY_DEPTH`, `DARK_BG` |
| クラス | PascalCase | `Prompt`, `PromptService` |
| プライベート | _ 接頭辞 | `_internal_method`, `_cache` |
| 特別なメソッド | ダブルアンダースコア | `__init__`, `__str__` |

### 7.2 プロンプト関連の命名
- `prompt_id` : プロンプトの一意識別子
- `prompt` : Prompt オブジェクト
- `prompts` : Prompt のリスト
- `category_ids` : ["cat1_id", "cat2_id", "cat3_id"] 形式のリスト（IDベース）

---

## 8. 設計原則

### 8.1 依存性注入
```python
class PromptService:
    """DataService を注入可能な設計。"""
    
    def __init__(self, data_service: DataService) -> None:
        self.data_service = data_service
    
    def create_prompt(self, **kwargs) -> Prompt:
        prompt = Prompt(**kwargs)
        self.data_service.save(prompt)
        return prompt
```

### 8.2 グローバル変数・シングルトン禁止
- 状態は `AppState` で一元管理
- コンポーネント間のデータ共有はコンストラクタ経由

### 8.3 テスト容易性
```python
# 副作用を持つ処理と純粋な処理を分離
def validate_category_depth(category_ids: List[str]) -> bool:
    """純粋関数：ビジネスロジック。"""
    return len(category_ids) <= MAX_CATEGORY_DEPTH

class CategoryService:
    """副作用を含む操作はStateManagerに委譲。"""
    
    def create_category(self, name: str, parent_id: Optional[str]) -> Category:
        # Categoryオブジェクトを生成して返すだけ
        return Category(
            id=str(uuid.uuid4()),
            name=name,
            parent_id=parent_id,
            order=0
        )
```

---

## 9. Flet 0.28.3 との互換性

### 9.1 使用可能な API
- `flet` : 推奨
- 新規 API はバージョン確認必須

### 9.2 非推奨 API の確認
AIに指示する際は以下を明記：
```
「Flet 0.28.3 の最新 API を使用してください」
「0.28.3 で廃止された API は使わないでください」
```

### 9.3 バージョン情報の記載
```python
import flet as ft

# Flet バージョンの確認
print(f"Flet version: {ft.__version__}")  # 0.28.3 を期待

# Python バージョンの確認
import sys
print(f"Python version: {sys.version_info}")  # 3.14.2 以上を期待
```

---

## 10. AI への指示テンプレート

AIに指示する際は、以下の項目を含める：

```
【Python コーディング依頼】

バージョン：
- Python 3.14.2
- Flet 0.28.3

ファイル：[ファイルパスと役割]

要件：
[実装内容]

規約厳守事項：
- 型ヒント：すべての関数に Optional/Union/List などを明記
- Docstring：Google Style で記載
- 定数：config.py または ui/styles/ に配置
- エラー：logger.error() でコンソール出力
- コメント：Docstring と明白でない処理のみ

参考：
- アーキテクチャ: docs/architecture.md
- 要件定義: docs/requirements.md
```

---

## 11. コードレビューチェックリスト

AI にコードを書かせたら、以下を確認：

- [ ] Python 3.14.2 との互換性
- [ ] Flet 0.28.3 との互換性
- [ ] すべての関数に型ヒント（Optional, Union, List など）
- [ ] すべての公開関数/クラスに Google Style Docstring
- [ ] エラーハンドリングと logger.error() の使用
- [ ] 定数が config.py または ui/styles/ に配置
- [ ] PEP 8 命名規則の準拠
- [ ] インポート順序が正しい
- [ ] グローバル変数・シングルトンがない
- [ ] 過度なコメントがない（Docstring で十分か）

---

## 12. 参考資料

- [PEP 8 – Style Guide for Python Code](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Flet Documentation](https://flet.dev/)
- [Python 3.14 Documentation](https://docs.python.org/3.14/)
