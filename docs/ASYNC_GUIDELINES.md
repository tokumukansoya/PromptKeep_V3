# Flet 非同期処理ガイドライン

## ⚠️ 重要：Fletにおける非同期処理の正しい実装方法

### 問題の背景

PromptKeepでは自動保存機能でデバウンス処理を実装する必要があります。Python標準の`asyncio`を使用しますが、**Fletアプリでは特別な注意が必要**です。

### ❌ 誤った実装（使用禁止）

```python
import asyncio

class StateManager:
    def _schedule_save(self):
        if self._save_task:
            self._save_task.cancel()
        # ❌ NG: asyncio.create_task()を直接使用
        self._save_task = asyncio.create_task(self._debounced_save())
```

**問題点:**
- Fletは独自のイベントループを管理している
- `asyncio.create_task()`を直接使うと、Fletのイベントループと競合する可能性がある
- タスクのキャンセルやエラーハンドリングが不安定になる

### ✅ 正しい実装（推奨）

```python
class StateManager:
    def __init__(self, page: ft.Page, data_service: DataService):
        self._page = page  # pageインスタンスを保持
        self._save_task = None
        
    def _schedule_save(self):
        if self._save_task:
            self._save_task.cancel()
        # ✅ OK: page.run_task()を使用
        self._save_task = self._page.run_task(self._debounced_save)
    
    async def _debounced_save(self):
        await asyncio.sleep(self._debounce_seconds)
        self._data_service.save_data(self._state)
```

**利点:**
- Fletのイベントループと正しく統合される
- タスクの生存期間が適切に管理される
- エラーハンドリングがFletの標準的な方法に従う

## 📚 Flet公式ドキュメントの推奨パターン

### バックグラウンドタスクの実行

```python
# 推奨: page.run_task()を使用
def did_mount(self):
    self.running = True
    self.page.run_task(self.update_timer)

async def update_timer(self):
    while self.running:
        # 何かの処理
        await asyncio.sleep(1)
```

参考: https://flet.dev/docs/getting-started/async-apps#threading

### 非同期イベントハンドラ

```python
# イベントハンドラ内で非同期処理を呼ぶ場合
async def button_click(e):
    await some_async_method()
    page.add(ft.Text("Hello!"))

page.add(ft.ElevatedButton("Say hello!", on_click=button_click))
```

### スリープ処理

```python
# ✅ OK: asyncio.sleep()を使用（非同期関数内）
async def delayed_action(self):
    await asyncio.sleep(2)
    # 何かの処理

# ❌ NG: time.sleep()は使用しない（UIをブロックする）
def delayed_action(self):
    time.sleep(2)  # これは避ける
```

## 🎯 PromptKeepでの適用箇所

### 1. StateManager（自動保存のデバウンス）

```python
class StateManager:
    def __init__(self, page: ft.Page, data_service: DataService):
        self._page = page
        # ...
    
    def _schedule_save(self):
        # page.run_task()を使用
        self._save_task = self._page.run_task(self._debounced_save)
```

### 2. その他のバックグラウンド処理

将来的に以下のような機能を追加する場合も同じパターンを使用：

- 定期的なバックアップ作成
- 自動同期処理
- プログレスバーのアニメーション
- カウントダウンタイマー

## 🔧 実装時のチェックリスト

- [ ] StateManagerの`__init__`に`page: ft.Page`パラメータを追加
- [ ] `_schedule_save()`で`page.run_task()`を使用
- [ ] `asyncio.create_task()`の直接使用を避ける
- [ ] 非同期処理が必要な場合は`async def`で定義
- [ ] `asyncio.sleep()`を使用（`time.sleep()`は使用しない）

## 📖 参考資料

- [Flet Async Apps - 公式ドキュメント](https://flet.dev/docs/getting-started/async-apps)
- [page.run_task() API リファレンス](https://flet.dev/docs/controls/page#run_taskhandler-args-kwargs)
- Python asyncio公式ドキュメント: https://docs.python.org/3/library/asyncio.html

---

**最終更新**: 2025-12-27  
**作成者**: AI実装ガイド更新
