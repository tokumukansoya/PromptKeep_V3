# PromptKeep - クイックスタートガイド

このガイドは、PromptKeepの開発を**すぐに始める**ための最短手順です。

---

## 🚀 5分でセットアップ

### 1. リポジトリのクローン

```bash
cd /path/to/workspace
git clone https://github.com/yourusername/PromptKeep_V3.git
cd PromptKeep_V3
```

### 2. uvのインストール（初回のみ）

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. 依存関係のインストール

```bash
uv sync
```

### 4. アプリ起動確認

```bash
uv run python main.py
```

✅ ウィンドウが開けば成功！

---

## 📚 実装を始める前に

### 必読ドキュメント（5分）

1. **[.clinerules](.clinerules)** - Roo Code設定（全体ルール）
2. **[docs/ai_execution_guide.md](docs/ai_execution_guide.md)** - Phase別実行ガイド
3. **[docs/coding_style.md](docs/coding_style.md)** - コーディング規約

### ドキュメント構成の理解（2分）

```
.clinerules                    ← Roo Code設定・全体ルール
docs/
  ├── ai_execution_guide.md    ← 実装時の最優先ガイド ⭐️
  ├── coding_style.md          ← コーディング規約
  ├── requirements.md          ← 機能要件
  ├── architecture.md          ← アーキテクチャ
  ├── implementation_plan.md   ← 実装計画
  └── DOCUMENT_GUIDE.md        ← ドキュメント案内
```

---

## 🎯 実装フロー（Roo Code）

### Phase実装の標準フロー

```bash
# 1. 最新のmainブランチに移動
git checkout main
git pull origin main

# 2. Phase用のブランチを作成
git checkout -b phase-N-description

# 3. ai_execution_guide.md を開く
cat docs/ai_execution_guide.md

# 4. 該当Phaseの「🤖 AI実行コマンド」をコピー
#    例: Phase 2-1: CategoryService 実装

# 5. Roo Codeに貼り付けて実行

# 6. 実装完了後、コミット
git add services/category_service.py
git commit -m "feat: Phase 2-1 CategoryService 実装完了"

# 7. 成功確認チェックリストで検証
#    「✅ 成功確認チェックリスト」を確認

# 8. Phase完了したらmainにマージ
git checkout main
git merge phase-N-description
git push origin main
git branch -d phase-N-description

# 9. 次のPhaseへ
```

---

## 🔧 よく使うコマンド

### パッケージ管理

```bash
# パッケージ追加
uv add <package-name>

# 開発用パッケージ追加
uv add --dev <package-name>

# 依存関係の同期
uv sync

# バージョン確認
uv run python -c "import flet; print(flet.__version__)"
```

### 実行・デバッグ

```bash
# 通常実行
uv run python main.py

# 開発モード（ホットリロード）
uv run flet run main.py

# Ruff（Linter + Formatter）
uv run ruff check .              # Lintチェック
uv run ruff check --fix .        # 自動修正
uv run ruff format .             # フォーマット

# 型チェック
uv run mypy services/category_service.py

# テスト実行
uv run pytest tests/
```

### Git操作

```bash
# ステータス確認
git status

# 変更をステージング
git add <file>

# コミット
git commit -m "feat: 説明"

# ブランチ一覧
git branch

# ブランチ切り替え
git checkout <branch-name>

# マージ
git merge <branch-name>
```

---

## 📋 実装チェックリスト

Phase実装時、以下を必ず確認してください：

### 実装前
- [ ] ai_execution_guide.md で該当Phaseを確認した
- [ ] 依存するPhaseが完了している
- [ ] gitブランチを作成した (`git checkout -b phase-N-...`)

### コーディング中
- [ ] 型ヒントを付けている（すべての関数・引数・戻り値）
- [ ] Google Style Docstringを書いている
- [ ] config.py から定数を読み込んでいる
- [ ] logger.info/error() を使っている
- [ ] エラーハンドリングを実装している

### 実装後
- [ ] 成功確認チェックリストが全て✅
- [ ] エラーなく実行できる (`uv run python main.py`)
- [ ] git commit を実行した
- [ ] 次のPhaseの依存関係を満たしている

---

## ⚠️ よくある失敗と対策

### 1. 型ヒントを忘れる

```python
# ❌ NG
def create_prompt(title, body):
    ...

# ✅ OK
def create_prompt(title: str, body: str) -> Prompt:
    ...
```

### 2. config.py を使わない

```python
# ❌ NG
MAX_DEPTH = 3  # ファイル内でハードコード

# ✅ OK
from config import MAX_CATEGORY_DEPTH
```

### 3. print() を使う

```python
# ❌ NG
print("エラーが発生しました")

# ✅ OK
from utils.logger import logger
logger.error("エラーが発生しました")
```

### 4. Gitコミットを忘れる

```bash
# ファイルを作成したら必ずコミット
git add services/new_service.py
git commit -m "feat: Phase X-Y NewService 実装完了"
```

### 5. Phase依存を無視する

Phase 4（UIコア）を実装する前に、Phase 1〜3が完了している必要があります。
→ `docs/implementation_plan.md` の依存関係図を確認

---

## 🆘 困ったときは

### エラーが出た
1. エラーメッセージを確認
2. [docs/coding_style.md](docs/coding_style.md) を再確認
3. [docs/ai_execution_guide.md](docs/ai_execution_guide.md) の該当Phaseを確認

### 仕様がわからない
1. [docs/requirements.md](docs/requirements.md) を確認
2. データ制約・機能要件を確認

### 設計がわからない
1. [docs/architecture.md](docs/architecture.md) を確認
2. ディレクトリ構造・クラス設計を確認

### 次に何をすればいいかわからない
1. [docs/implementation_plan.md](docs/implementation_plan.md) を確認
2. 依存関係図で次のPhaseを確認

---

## 📞 サポート

質問・相談は以下へ：
- GitHub Issues: （リポジトリURL）/issues
- ドキュメント: [docs/DOCUMENT_GUIDE.md](docs/DOCUMENT_GUIDE.md)

---

**これで準備完了です！さっそく実装を始めましょう 🚀**

次のステップ: [docs/ai_execution_guide.md](docs/ai_execution_guide.md) を開いて、Phase 2-1から始めてください。
