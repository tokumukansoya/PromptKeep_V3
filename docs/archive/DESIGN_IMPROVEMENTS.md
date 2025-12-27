# 設計改善実施サマリー（2025-12-27）

本ドキュメントは、PromptKeep V3の設計上の不備を修正した内容をまとめたものです。

---

## 🎯 改善実施項目（全8項目）

### ✅ 1. 状態管理の方針明確化（重要度：高）

**問題点:**
- AppStateがミュータブルなのに「イミュータブル更新」と矛盾
- 各Controllerが直接状態を操作できる設計は一貫性を保つのが困難

**修正内容:**
- `services/state_manager.py` を新規作成
- StateManagerパターンを採用
  - 全ての状態変更はStateManagerを経由
  - デバウンス付き自動保存を内包
  - リスナーパターンでUI更新を通知
- `models/app_state.py` のドキュメントを更新
  - 「StateManagerを経由して状態変更する」ことを明記

**影響範囲:**
- `docs/architecture.md` - StateManager方式の説明追加
- `docs/requirements.md` - 自動保存ロジックをStateManager実装に変更
- `docs/implementation_plan.md` - Phase 2の実装内容を更新

---

### ✅ 2. サービス層の責務分離（重要度：中）

**問題点:**
- PromptServiceとDataServiceの境界が不明瞭
- データ永続化のタイミング制御が分散

**修正内容:**
- 責務を明確に分離:
  - **StateManager**: 状態管理・永続化・通知の統括
  - **PromptService/CategoryService**: ビジネスロジックのみ（純粋関数）
  - **DataService**: JSON読み書きの低レベル操作

**データフロー:**
```
Controller → Service（ビジネスロジック） → StateManager（状態更新+自動保存） → UI更新
```

**影響範囲:**
- `docs/architecture.md` - 各層の責務を明確化
- `docs/implementation_plan.md` - Phase 2の実装順序を更新

---

### ✅ 3. category_path設計変更（重要度：高）

**問題点:**
- `category_path: List[str]`（カテゴリ名の配列）だと、カテゴリ名変更時に全プロンプトを更新必要
- カテゴリ削除時の整合性チェックが複雑

**修正内容:**
- **`category_path` → `category_ids`** に変更
- カテゴリIDの配列に変更: `["cat1_id", "cat2_id", "cat3_id"]`
- カテゴリ名変更時もプロンプトは影響を受けない

**修正ファイル:**
- ✅ `models/prompt.py` - フィールド名変更、ドキュメント更新
- ✅ `docs/requirements.md` - JSONスキーマ更新、制約表更新
- ✅ `docs/architecture.md` - モデル定義更新
- ✅ `docs/coding_style.md` - サンプルコード更新

---

### ✅ 4. エラーハンドリング戦略の具体化（重要度：中）

**問題点:**
- `exceptions.py`に具体的な例外実装が不足
- ユーザー向けメッセージの統一的な管理がない

**修正内容:**
- 基底例外クラスに`user_message`属性を追加:
  ```python
  class PromptKeeperError(Exception):
      def __init__(self, message: str, user_message: str | None = None):
          self.user_message = user_message or message
  ```
- 各例外クラスに具体的な実装を追加:
  - `InvalidCategoryDepthError` - 階層エラーメッセージ自動生成
  - `DataPersistenceError` - 保存失敗時のメッセージ

**修正ファイル:**
- ✅ `exceptions.py` - 全例外クラスを実装
- ✅ `docs/architecture.md` - エラーハンドリングパターンを追加

---

### ✅ 5. UI層の過剰分割の簡素化（重要度：低）

**問題点:**
- 28個ものファイルに分割されたUI構造は初期段階では過剰
- 特に`card/`配下の4ファイル分割は不要

**修正内容:**
- UI構造を簡素化:
  ```
  card/
  ├── prompt_card.py  # 統合（ヘッダー・本文・アクション全て含む）
  
  sidebar/
  ├── sidebar.py
  └── category_tree.py  # 検索機能込み
  ```

**影響範囲:**
- ✅ `docs/architecture.md` - UIコンポーネント構造を簡素化

---

### ✅ 6. Undo機能の方針明確化（重要度：低）

**問題点:**
- 「削除のみ・1ステップのみ」という制約が中途半端

**修正内容:**
- Phase 2で「削除のUndo」を実装
- **Phase 12をUndo拡張フェーズに変更**（オプション・低優先度）
  - Commandパターンの検討
  - 複数操作のUndo対応
  - 必須ではなく、ゴミ箱機能で代替可能

**影響範囲:**
- ✅ `docs/implementation_plan.md` - Phase 12の内容を更新

---

### ✅ 7. パフォーマンス対策の追加（重要度：中）

**問題点:**
- 1000件のプロンプト全件表示は重い
- 検索の全件スキャンは非効率

**修正内容:**
- パフォーマンス対策を要件に追加:
  - カードグリッド: **ページネーション（50件/ページ）** または仮想スクロール
  - 検索インデックス: カテゴリ・お気に入りのインデックス構造
  - 1,000件超えの場合はページネーション採用

**影響範囲:**
- ✅ `docs/requirements.md` - パフォーマンス対策を追加
- ✅ `docs/implementation_plan.md` - Phase 13にパフォーマンステスト追加

---

### ✅ 8. テスト戦略の具体化（重要度：低）

**問題点:**
- 「可能な範囲で」という表現が具体性に欠ける

**修正内容:**
- Phase 13（旧Phase 12）に具体的なテスト内容を追加:
  - 統合テスト（手動）
  - エッジケースの確認
  - **パフォーマンステスト（1000件超）**
  - ページネーション動作確認

**影響範囲:**
- ✅ `docs/implementation_plan.md` - Phase 13の内容を具体化

---

## 📁 修正ファイル一覧

### コードファイル
1. ✅ `models/prompt.py` - category_path → category_ids に変更
2. ✅ `models/app_state.py` - StateManager方式のドキュメント更新
3. ✅ `exceptions.py` - user_message機能追加、各例外クラス実装
4. ✅ `services/state_manager.py` - **新規作成**

### ドキュメントファイル
5. ✅ `docs/requirements.md` - category_ids更新、StateManager実装例追加、パフォーマンス対策追加
6. ✅ `docs/architecture.md` - StateManager追加、UI簡素化、エラーハンドリング追加
7. ✅ `docs/implementation_plan.md` - Phase 2更新、Phase 12→13再編成
8. ✅ `docs/coding_style.md` - category_ids更新

---

## 🚀 次のステップ

### 実装前に確認すべき事項
1. **StateManagerの設計理解**: 全ての状態変更がStateManagerを経由することを確認
2. **category_idsの理解**: カテゴリ名ではなくIDを使用することを確認
3. **エラーハンドリング**: user_messageを活用したUI通知を実装

### Phase 0.5実行準備
```bash
# 開発ツールのセットアップ
uv add --dev ruff
uv add loguru

# utils/logger.py作成
# .vscode/settings.json作成（既存）

# 検証
uv run ruff check .
uv run python -c "from utils.logger import logger; logger.info('Test')"
```

---

## ✅ 改善完了チェックリスト

- [x] 状態管理の方針明確化（StateManager方式）
- [x] category_path → category_ids変更
- [x] エラーハンドリング強化（user_message）
- [x] UI構造の簡素化
- [x] パフォーマンス対策の追加
- [x] Undo機能の方針明確化
- [x] テスト戦略の具体化
- [x] 全ドキュメントの整合性確認

**全ての設計上の不備は修正完了しました。実装を開始できます。**
