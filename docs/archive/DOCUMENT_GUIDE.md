# PromptKeep ドキュメントガイド

このドキュメントは、PromptKeepプロジェクトの各種ドキュメントの役割と参照順序を説明します。

---
## 📖 ドキュメント駆動開発の原則

### ⭐️ 金科玉条: ドキュメントファースト

新機能追加・仕様変更の際は、**必ずドキュメントを先に更新**してからコードを書く。

```
1. ドキュメント更新 → Gitコミット
2. コード実装 → Gitコミット
```

詳細は [.clinerules](../.clinerules) と [ai_execution_guide.md](ai_execution_guide.md) を参照。

---
## 📋 ドキュメント一覧と役割

### 🎯 実装・開発時に参照するドキュメント

#### 1. [ai_execution_guide.md](ai_execution_guide.md) ⭐️ 最優先
**対象**: Roo Code / GitHub Copilot / AI開発者

**内容**:
- Phase別の完全な実行コマンド
- 検証可能な成功基準チェックリスト
- コード例・実装パターン
- エラーハンドリング方法
- 依存関係マップ

**いつ使う**: 実装を開始する前に必ず確認

---

#### 2. [coding_style.md](coding_style.md)
**対象**: すべての開発者・AI

**内容**:
- Python 3.14.2 / Flet 0.28.3 のバージョン指定
- 型ヒント・Docstringの書き方（Google Style）
- ファイル構成・インポート順序
- 命名規則
- エラーハンドリング規約

**いつ使う**: コードを書く前と後（品質チェック）

---

#### 3. [requirements.md](requirements.md)
**対象**: すべての開発者・AI

**内容**:
- 機能要件（優先度順）
- データモデル定義（JSON スキーマ）
- データ制約（カテゴリは1階層、文字数など）
- 非機能要件（パフォーマンス、アクセシビリティ）
- 画面・コンポーネント要件
- 状態管理・振る舞いの詳細
- エラーハンドリングパターン

**いつ使う**: 
- 実装内容を確認する時
- 機能の仕様を調べる時
- 制約条件を確認する時

---

#### 4. [architecture.md](architecture.md)
**対象**: すべての開発者・AI

**内容**:
- ディレクトリ構造（完全版）
- 各層の責務（models, services, ui, utils）
- データフロー図
- 主要なクラス定義
- コンポーネント間の依存関係

**いつ使う**:
- プロジェクト全体の構造を理解する時
- 新しいファイルを作成する場所を決める時
- クラス設計を確認する時

---

#### 5. [implementation_plan.md](implementation_plan.md)
**対象**: すべての開発者

**内容**:
- Phase別の実装計画（Phase 0〜12）
- 各Phaseの依存関係
- 実装順序の推奨
- 検証可能な成功基準（Phase 0〜2のみ詳細）
- マイルストーン定義

**いつ使う**:
- プロジェクトの進捗を把握する時
- 次に何を実装すべきか確認する時
- 並列実装可能なPhaseを探す時

---

#### 6. [ai_prompts.md](ai_prompts.md)
**対象**: AI（補助的）

**内容**:
- Phase別のテンプレート集
- コピペ用のプロンプト

**いつ使う**:
- ai_execution_guide.md に記載のないPhaseを実装する時
- 既存テンプレートをカスタマイズする時

---

### 🔧 開発フロー・運用系ドキュメント

#### 7. [.clinerules](../.clinerules) ⭐️ Roo Code設定
**対象**: Roo Code / Cline AI

**内容**:
- プロジェクト概要
- 環境管理ルール（uv使用）
- コーディング規約のサマリー
- Git運用ルール（必須）
- コミットタイミング
- コミットメッセージ規則
- 実装フロー
- 検証コマンド

**いつ使う**: Roo Code起動時に自動読込（常時参照）

---

#### 8. [git_workflow.md](git_workflow.md)
**対象**: すべての開発者

**内容**:
- Gitブランチ戦略
- コミットメッセージ規則
- Phase別のブランチ作成方法
- マージフロー

**いつ使う**: Git操作の詳細を確認する時（.clinerules に基本ルールあり）

---

### 📖 プロジェクト概要

#### 9. [README.md](../README.md)
**対象**: 初めてプロジェクトを見る人

**内容**:
- プロジェクト概要
- セットアップ手順
- 実行方法
- ドキュメント駆動開発の説明

**いつ使う**: プロジェクトの最初の理解

---

## 🚀 開発フロー（推奨）

### Roo Code / AI による自動実装

```
1. README.md を読む（プロジェクト概要を理解）
   ↓
2. ai_execution_guide.md を開く（実装ガイド確認）
   ↓
3. 実装したいPhaseのセクションを見つける
   ↓
4. 「🤖 AI実行コマンド」をコピー＆ペースト
   ↓
5. AIがコードを生成
   ↓
6. 「✅ 成功確認チェックリスト」で検証
   ↓
7. coding_style.md でコード品質を確認
   ↓
8. 次のPhaseへ
```

### 手動実装

```
1. README.md を読む（プロジェクト概要を理解）
   ↓
2. architecture.md を読む（全体構造を理解）
   ↓
3. requirements.md で機能要件を確認
   ↓
4. implementation_plan.md で実装順序を確認
   ↓
5. coding_style.md を確認しながらコーディング
   ↓
6. git_workflow.md に従ってコミット
   ↓
7. 次のPhaseへ
```

---

## 📊 ドキュメント更新ガイド

### 優先度

| ドキュメント | 更新頻度 | 更新タイミング |
|------------|---------|--------------|
| ai_execution_guide.md | 高 | 新Phase追加時、実装パターン変更時 |
| requirements.md | 中 | 機能要件変更時 |
| coding_style.md | 低 | 規約変更時 |
| architecture.md | 低 | 設計変更時 |
| implementation_plan.md | 中 | Phase完了時、計画変更時 |

### 更新ルール

1. **ai_execution_guide.md を最優先で更新**
   - 新しいPhaseを追加する際は必ず更新
   - 実行コマンドと成功確認チェックリストを必ず記載

2. **requirements.md は仕様変更時のみ**
   - 機能の追加・削除があった場合
   - データ制約が変わった場合

3. **実装完了後は implementation_plan.md を更新**
   - Phaseの状態を「✅ 完了」にマーク
   - 検証結果を記録

---

## ❓ よくある質問

### Q1: どのドキュメントから読めばいい？
**A**: Roo Codeで実装する場合は [ai_execution_guide.md](ai_execution_guide.md) を最初に読んでください。全体像を把握したい場合は [README.md](../README.md) → [architecture.md](architecture.md) の順がおすすめです。

### Q2: ai_execution_guide.md と ai_prompts.md の違いは？
**A**: `ai_execution_guide.md` が**メインドキュメント**で、詳細な実行コマンドと検証基準が記載されています。`ai_prompts.md` は補助的なテンプレート集で、カスタマイズ用です。

### Q3: コーディング規約がわからない
**A**: [coding_style.md](coding_style.md) を参照してください。型ヒント、Docstring、命名規則などすべて記載されています。

### Q4: カテゴリの最大階層は？
**A**: 本仕様ではカテゴリはフラット（1階層）です。詳細は [requirements.md](requirements.md) の「5.3 シンプルなカテゴリ管理」を参照。

### Q5: 次に何を実装すればいい？
**A**: [implementation_plan.md](implementation_plan.md) の「依存関係図」を確認してください。Phase 0-3が完了している場合、Phase 4（UIコアコンポーネント）に進めます。

---

## 🎓 学習リソース

### Flet 公式ドキュメント
- https://flet.dev/docs/

### Python 型ヒント
- https://docs.python.org/ja/3/library/typing.html

### Google Style Docstring
- https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings

---

**最終更新**: 2025-12-27
