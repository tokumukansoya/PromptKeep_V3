# PromptKeep

プロンプトをローカルで安全に管理・閲覧・編集・コピーするシンプルなデスクトップアプリケーション。

**Version**: 1.0.0  
**Status**: 開発中（データ層・ビジネスロジック層完成、UI 実装予定）

---

## 概要

PromptKeep は、AI プロンプトを効率的に管理するために設計されたデスクトップアプリです。

**主な機能:**
- 📝 プロンプト作成・編集・削除
- 🏷️ 階層カテゴリ（最大 3 階層）による整理
- ⭐ お気に入り機能
- 📋 プロンプト内容のワンクリックコピー
- 🗑️ ゴミ箱機能（復元可能）
- ↩️ Ctrl+Z アンドゥ機能
- 🔍 タイトル・本文での検索

**技術スタック:**
- Python 3.14.2
- Flet 0.28.3（UI フレームワーク）
- JSON（ローカルデータ永続化）

---

## セットアップ

### 前提条件
- Python 3.14.2 以上
- pip

### インストール手順

```bash
# リポジトリをクローン
cd PromptKeep_V3

# 仮想環境を作成
python -m venv .venv

# 仮想環境を有効化
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 依存パッケージをインストール
pip install -r requirements.txt
```

### アプリケーション起動

```bash
python main.py
```

---

## ディレクトリ構成

```
PromptKeep_V3/
├── main.py                          # アプリケーション エントリーポイント
├── config.py                        # アプリケーション設定定数
├── requirements.txt                 # 依存パッケージ
├── exceptions.py                    # カスタム例外クラス
│
├── data/                            # データディレクトリ（自動生成）
│   ├── prompts.json                 # プロンプトデータ
│   └── backup/                      # バックアップファイル
│
├── docs/                            # ドキュメント
│   ├── requirements.md              # 要件定義
│   ├── architecture.md              # アーキテクチャ設計
│   ├── coding_style.md              # コーディング規約
│   └── implementation_plan.md       # 実装計画（ロードマップ）
│
├── models/                          # データモデル層
│   ├── prompt.py                    # Prompt クラス
│   ├── category.py                  # Category クラス
│   └── app_state.py                 # AppState（全体状態）
│
├── services/                        # ビジネスロジック層
│   ├── data_service.py              # JSON 読み書き
│   ├── prompt_service.py            # プロンプト CRUD
│   ├── category_service.py          # カテゴリ CRUD（実装予定）
│   ├── undo_service.py              # アンドゥ管理（実装予定）
│   ├── clipboard_service.py         # クリップボード操作（実装予定）
│   └── search_service.py            # 検索・フィルタ（実装予定）
│
├── ui/                              # UI 層（実装予定）
│   ├── app.py                       # Flet アプリケーション
│   │
│   ├── views/                       # 画面・ビュー
│   │   ├── main_view.py
│   │   ├── card_grid_view.py
│   │   ├── edit_view.py
│   │   └── trash_view.py
│   │
│   ├── components/                  # UI コンポーネント
│   │   ├── card/
│   │   ├── sidebar/
│   │   ├── editor/
│   │   ├── dialogs/
│   │   └── common/
│   │
│   ├── controllers/                 # UI イベントハンドラ
│   │   ├── main_controller.py
│   │   ├── card_controller.py
│   │   ├── edit_controller.py
│   │   └── keyboard_controller.py
│   │
│   └── styles/                      # UI スタイル定数
│       ├── colors.py                # カラーパレット
│       ├── typography.py            # フォント定義
│       ├── spacing.py               # 余白・サイズング
│       └── card_style.py            # カードスタイル
│
└── utils/                           # ユーティリティ関数
    ├── text_utils.py                # テキスト処理
    ├── date_utils.py                # 日時処理
    └── file_utils.py                # ファイル操作
```

---

## 実装ロードマップ

| Phase | 機能 | ステータス | 予定 |
|-------|------|----------|------|
| **0** | 環境セットアップ、スケルトンコード | ✅ 完了 | — |
| **1** | データモデル、AppState | ✅ 完了 | — |
| **2** | ビジネスロジック（PromptService）| ✅ 完了 | — |
| **3** | UI スタイル定義 | ✅ 完了 | — |
| **4** | コアコンポーネント（カード表示）| ⏳ 実装予定 | Phase 5 に依存 |
| **5** | 編集機能・自動保存 | ⏳ 実装予定 | Phase 4 に依存 |
| **6** | カテゴリ管理（D&D）| ⏳ 実装予定 | Phase 5 に依存 |
| **7** | メイン画面統合 | ⏳ 実装予定 | Phase 4-6 に依存 |
| **8** | ゴミ箱機能 | ⏳ 実装予定 | Phase 7 に依存 |
| **9** | キーボード操作（Ctrl+Z など） | ⏳ 実装予定 | Phase 7 に依存 |
| **10** | 検索・フィルタ機能 | ⏳ 実装予定 | Phase 7 に依存 |
| **11** | エラーハンドリング・ロギング | ⏳ 実装予定 | Phase 7 に依存 |
| **12** | テスト・最適化 | ⏳ 実装予定 | 最終段階 |

詳細は [docs/implementation_plan.md](docs/implementation_plan.md) を参照。

---

## 開発者ガイド

### ドキュメント参照順序

1. **要件定義** → [docs/requirements.md](docs/requirements.md)
   - 機能仕様、UI/UX 設計

2. **アーキテクチャ** → [docs/architecture.md](docs/architecture.md)
   - ディレクトリ構成、データフロー、クラス設計

3. **コーディング規約** → [docs/coding_style.md](docs/coding_style.md)
   - 型ヒント、Docstring、命名規則、バージョン厳守

4. **実装計画** → [docs/implementation_plan.md](docs/implementation_plan.md)
   - Phase ごとの実装内容、AI 指示テンプレート

### AI に指示する際の方法

#### ステップ 1: テンプレートを用意

```markdown
【Phase X: [フェーズ名] 実装】

バージョン：
- Python 3.14.2
- Flet 0.28.3

対象ファイル：
- models/xxx.py
- services/xxx.py
- ...

要件：
- [実装内容]

依存：Phase Y の完成を前提

規約厳守事項：
- 型ヒント：すべての関数に Optional/Union/List などを明記
- Docstring：Google Style で記載
- 定数：config.py または ui/styles/ に配置
- エラー：logger.error() でコンソール出力
- コメント：Docstring と明白でない処理のみ

参考ドキュメント：
- アーキテクチャ: docs/architecture.md
- 要件定義: docs/requirements.md
- コーディング規約: docs/coding_style.md
- 実装計画: docs/implementation_plan.md
```

#### ステップ 2: 指示をコピペ

テンプレートを Copilot / Roo Code にコピペして実行。

#### ステップ 3: コード確認

- [ ] 型ヒントが完全か
- [ ] Docstring は Google Style か
- [ ] エラーハンドリングと logger.error() の使用
- [ ] 定数は config.py または ui/styles/ に配置されているか
- [ ] Python 3.14.2、Flet 0.28.3 対応か

#### ステップ 4: コードレビューチェックリスト

[docs/coding_style.md](docs/coding_style.md) の「コードレビューチェックリスト」を参照。

### ローカル開発フロー

```bash
# 1. 仮想環境を有効化
.venv\Scripts\activate  # Windows
# または
source .venv/bin/activate  # macOS/Linux

# 2. ファイルを編集

# 3. 現在の状態を確認
python main.py

# 4. AI に指示（テンプレート使用）

# 5. 生成されたコードをコミット
```

---

## トラブルシューティング

### Python バージョンエラー

**エラー:**
```
SystemExit: Python 3.14以上が必要です（現在: 3.x.x）
```

**原因:**
- Python バージョンが 3.14 未満

**対応:**
```bash
# Python 3.14.2 をインストール
# https://www.python.org/downloads/

# インストール後、バージョン確認
python --version

# 仮想環境を再作成
rm -r .venv
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Flet バージョンエラー

**エラー:**
```
Flet version mismatch: expected 0.28.3, got X.X.X
```

**原因:**
- Flet のバージョンが 0.28.3 以外

**対応:**
```bash
# 正しいバージョンをインストール
pip install flet==0.28.3

# バージョン確認
pip show flet
```

### ImportError: No module named 'flet'

**原因:**
- 仮想環境が有効化されていない
- 依存パッケージがインストールされていない

**対応:**
```bash
# 1. 仮想環境を有効化
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# 2. 依存パッケージをインストール
pip install -r requirements.txt

# 3. 動作確認
python main.py
```

### JSON データ読み込みエラー

**エラー:**
```
InvalidDataError: JSON の形式が不正です
```

**原因:**
- `data/prompts.json` が破損している
- 手動編集で不正な JSON 形式になっている

**対応:**
```bash
# バックアップから復元
python -c "
from services.data_service import DataService
ds = DataService()
ds.restore_from_backup()
print('Restored from backup')
"

# または、古いファイルを削除して再作成
rm data/prompts.json
python main.py
```

### ファイルパーミッションエラー

**エラー:**
```
PermissionError: [Errno 13] Permission denied
```

**原因:**
- `data/` ディレクトリが読み書き不可

**対応:**
```bash
# Windows
icacls data /grant %USERNAME%:F /t

# macOS/Linux
chmod -R u+w data/
```

---

## よくある質問

**Q: UI はいつ実装されますか？**  
A: 実装計画は [docs/implementation_plan.md](docs/implementation_plan.md) を参照。Phase 4 から UI 実装が始まります。

**Q: AI に指示する際、何をコピペすればいい？**  
A: 上記「AI に指示する際の方法」セクションのテンプレートを参照。

**Q: ローカルデータ以外に保存できる？**  
A: 現在は JSON ファイルのみ。クラウド連携は将来の検討対象。

**Q: 既存のプロンプトをインポートできる？**  
A: 現在は未実装。CSV/JSON インポート機能は Phase 検討予定。

---

## ライセンス

個人用プロジェクト。

---

## サポート

問題が発生した場合：

1. [トラブルシューティング](#トラブルシューティング) を確認
2. [docs/coding_style.md](docs/coding_style.md) のエラーハンドリング セクションを確認
3. ログファイルを確認（コンソール出力）

---

## 次のステップ

- [ ] Phase 4 実装開始
- [ ] AI に Phase 4 を指示
- [ ] UI コンポーネントの完成
- [ ] メイン画面統合
- [ ] 全機能テスト・最適化
