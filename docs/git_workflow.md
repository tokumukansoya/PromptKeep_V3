# Git ワークフローガイド

このドキュメントは、PromptKeep 開発における Git の使い方を説明します。

---

## 📋 ブランチ戦略

### 基本方針

**Phase ごとにブランチを作成**し、完成後に main にマージします。

```
main (安定版・動作確認済み)
  ├── phase-2-services      # Phase 2 完了済み
  ├── phase-4-card-ui       # Phase 4 実装中
  ├── phase-5-editor        # Phase 5 実装中
  └── phase-6-sidebar       # Phase 6 実装中
```

### ブランチ命名規則

```
phase-{番号}-{概要}
```

**例:**
- `phase-4-card-ui`
- `phase-5-editor`
- `phase-6-sidebar`
- `phase-7-main-integration`

---

## 🚀 開発フロー

### 1. 初期セットアップ（最初の1回のみ）

```bash
# Git リポジトリの初期化（まだの場合）
git init

# .gitignore の確認
cat .gitignore

# 現在の状態をコミット
git add .
git commit -m "chore: 初期セットアップ完了（Phase 0-3）"

# main ブランチを確認
git branch -M main
```

---

### 2. Phase 開始時

```bash
# 最新の main に移動
git checkout main

# 新しい Phase ブランチを作成
git checkout -b phase-4-card-ui

# ブランチを確認
git branch
# * phase-4-card-ui
#   main
```

---

### 3. AI にコード生成させる

1. [docs/ai_prompts.md](ai_prompts.md) から該当 Phase のテンプレートをコピー
2. GitHub Copilot / Roo Code に貼り付け
3. AI がコードを生成
4. 生成されたコードを確認

---

### 4. コミット（小まめに行う）

#### コミット単位

**1つのコンポーネント = 1コミット** が理想

```bash
# Phase 4-1: CardBody 実装完了
git add ui/components/card/card_body.py
git commit -m "feat: Phase 4-1 CardBody コンポーネント実装"

# Phase 4-2: CardHeader 実装完了
git add ui/components/card/card_header.py
git commit -m "feat: Phase 4-2 CardHeader コンポーネント実装"

# Phase 4-3: PromptCard 実装完了
git add ui/components/card/prompt_card.py
git commit -m "feat: Phase 4-3 PromptCard コンポーネント実装"
```

#### コミットメッセージ規約

```
<type>: <subject>

[optional body]
```

**Type:**
- `feat`: 新機能実装
- `fix`: バグ修正
- `refactor`: リファクタリング
- `docs`: ドキュメント更新
- `style`: コードスタイル修正（機能変更なし）
- `test`: テスト追加・修正
- `chore`: その他（設定ファイルなど）

**例:**
```bash
git commit -m "feat: Phase 4-4 CardGridView 実装"
git commit -m "fix: カードのホバーエフェクト修正"
git commit -m "refactor: CardHeader のイベントハンドリング改善"
git commit -m "docs: README.md にセットアップ手順追加"
```

---

### 5. 動作確認

```bash
# アプリケーションを起動して動作確認
python main.py

# 問題があれば修正してコミット
git add .
git commit -m "fix: カード表示のレイアウト修正"
```

---

### 6. Phase 完成・main にマージ

#### Phase 完成のチェックリスト

- [ ] すべてのファイルが実装済み
- [ ] 動作確認済み（エラーなし）
- [ ] コーディング規約に準拠
- [ ] コミットメッセージが明確

#### マージ手順

```bash
# main ブランチに移動
git checkout main

# Phase ブランチをマージ（マージコミット作成）
git merge phase-4-card-ui --no-ff -m "Merge phase-4-card-ui: カード表示機能完成"

# マージ完了確認
git log --oneline --graph -5

# Phase ブランチを削除（オプション）
git branch -d phase-4-card-ui
```

**`--no-ff` の意味:**
- Fast-forward を禁止してマージコミットを明示的に作成
- Phase ごとの履歴が明確になる

---

### 7. 次の Phase へ

```bash
# 新しい Phase ブランチを作成
git checkout -b phase-5-editor

# 繰り返し...
```

---

## 🚨 トラブル時の対処法

### AI 生成コードが失敗した場合

#### パターン 1: 直前のコミットに戻る

```bash
# 最新のコミットを取り消す（変更は残る）
git reset --soft HEAD~1

# 最新のコミットを完全に取り消す（変更も破棄）
git reset --hard HEAD~1
```

#### パターン 2: ファイルだけ戻す

```bash
# 特定のファイルを前のコミットに戻す
git checkout HEAD -- ui/components/card/card_body.py

# すべての変更を破棄
git checkout -- .
```

#### パターン 3: ブランチごとやり直し

```bash
# main に戻る
git checkout main

# Phase ブランチを完全に削除
git branch -D phase-4-card-ui

# 新しい Phase ブランチを作成
git checkout -b phase-4-card-ui

# 再挑戦
```

---

### コミット間違えた場合

#### 直前のコミットメッセージを修正

```bash
git commit --amend -m "feat: Phase 4-1 CardBody コンポーネント実装（修正版）"
```

#### 直前のコミットにファイルを追加

```bash
# ファイルを追加
git add ui/components/card/card_body.py

# 直前のコミットに含める
git commit --amend --no-edit
```

---

### マージ前に確認したい場合

```bash
# main ブランチとの差分を確認
git diff main..phase-4-card-ui

# どのコミットがマージされるか確認
git log main..phase-4-card-ui --oneline

# マージのプレビュー（実際にはマージしない）
git merge phase-4-card-ui --no-commit --no-ff
git merge --abort  # 取り消し
```

---

## 📊 履歴の確認

### 基本コマンド

```bash
# コミット履歴を表示
git log --oneline

# グラフ表示
git log --oneline --graph --all

# 最新 10 件
git log --oneline -10

# Phase 4 のコミットのみ
git log --oneline --grep="Phase 4"
```

### ファイルの変更履歴

```bash
# 特定ファイルの履歴
git log --oneline -- ui/components/card/card_body.py

# ファイルの差分を表示
git log -p -- ui/components/card/card_body.py
```

---

## 🏷️ タグの活用（マイルストーン管理）

### タグとは

**特定のコミットに名前を付ける機能**。Phase 完成時にタグを打つと後で戻しやすい。

### タグの作成

```bash
# Phase 完成時にタグを作成
git tag phase-4-complete -m "Phase 4: カード表示機能完成"
git tag phase-5-complete -m "Phase 5: 編集機能完成"

# タグ一覧
git tag

# タグの詳細
git show phase-4-complete
```

### タグへの復帰

```bash
# タグの状態に戻る（確認のみ）
git checkout phase-4-complete

# タグの状態から新しいブランチを作成
git checkout -b bugfix-from-phase4 phase-4-complete
```

---

## 💾 バックアップ戦略

### ローカルバックアップ

```bash
# 現在のブランチを別名でバックアップ
git branch backup-phase-4 phase-4-card-ui

# バックアップ一覧
git branch | grep backup
```

### リモートリポジトリ（GitHub など）

```bash
# リモートリポジトリを追加
git remote add origin https://github.com/username/PromptKeep_V3.git

# main をプッシュ
git push -u origin main

# Phase ブランチもプッシュ
git push origin phase-4-card-ui

# タグもプッシュ
git push --tags
```

---

## 📝 よくある Git 操作

### 現在の状態を確認

```bash
# 変更されたファイルを確認
git status

# ブランチを確認
git branch

# 差分を確認
git diff
```

### 変更を一時保存（stash）

```bash
# 現在の変更を一時保存
git stash

# Phase を切り替え
git checkout main

# 保存した変更を復元
git checkout phase-4-card-ui
git stash pop
```

### ファイルを Git 管理から除外

```bash
# .gitignore に追加
echo "data/prompts.json" >> .gitignore

# すでに追跡されているファイルを除外
git rm --cached data/prompts.json
git commit -m "chore: prompts.json を Git 管理から除外"
```

---

## 🎯 推奨ワークフロー（まとめ）

```bash
# 1. Phase 開始
git checkout main
git checkout -b phase-X-feature

# 2. AI にコード生成させる（ai_prompts.md 使用）

# 3. コミット（小まめに）
git add <files>
git commit -m "feat: Phase X-Y 実装"

# 4. 動作確認
python main.py

# 5. 問題なければマージ
git checkout main
git merge phase-X-feature --no-ff

# 6. タグを作成（オプション）
git tag phase-X-complete

# 7. ブランチ削除（オプション）
git branch -d phase-X-feature

# 8. 次の Phase へ
git checkout -b phase-Y-next-feature
```

---

## 📚 参考資料

- [Git 公式ドキュメント](https://git-scm.com/doc)
- [Git ブランチ戦略](https://git-scm.com/book/ja/v2/Git-のブランチ機能-ブランチとマージの基本)
- [コミットメッセージ規約](https://www.conventionalcommits.org/ja/v1.0.0/)

---

## ✅ チェックリスト

Phase 完成時の確認：

- [ ] すべてのファイルが実装済み
- [ ] 動作確認済み（`python main.py` でエラーなし）
- [ ] コーディング規約に準拠（[docs/coding_style.md](coding_style.md)）
- [ ] コミットメッセージが明確
- [ ] main にマージ済み
- [ ] タグ作成済み（オプション）
- [ ] Phase ブランチ削除済み（オプション）

---
 
**次のステップ:** Phase 2（残りサービス）を完了してから Phase 4 に着手

推奨の進め方（コマンド例）:

```bash
# Phase 2 の残りサービスを実装するブランチを作成
git checkout main
git checkout -b phase-2-services

# 実装順の目安：CategoryService → UndoService → ClipboardService → SearchService
# 各コンポーネントごとに小まめにコミット

# Phase 2 完了後に main へ統合
git checkout main
git merge phase-2-services --no-ff -m "Merge phase-2-services: Phase 2 完了"
git tag phase-2-complete -m "Phase 2: サービス層が完成"

# 続いて Phase 4（カードUI）へ
git checkout -b phase-4-card-ui
```
