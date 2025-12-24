from __future__ import annotations

from typing import Callable, Dict, List, Optional

import flet as ft

from models.category import Category


class CategorySelector(ft.Dropdown):
    """カテゴリ選択用ドロップダウン。

    階層カテゴリをフラットなリストとして表示し、"親 > 子 > 孫" 形式で選択する。
    """

    def __init__(
        self,
        categories: List[Category],
        selected_path: List[str],
        on_change: Callable[[List[str]], None],
    ) -> None:
        """初期化。

        Args:
            categories: 表示するカテゴリ一覧。
            selected_path: 現在選択中のカテゴリ階層（例: ["親", "子"]）。
            on_change: 選択変更時にカテゴリ階層のリストを返すコールバック。
        """
        super().__init__()
        self._categories: List[Category] = categories
        self._on_change: Callable[[List[str]], None] = on_change

        # ドロップダウン設定
        self.label = "カテゴリ"
        self.options = self._build_options()
        self.value = self._path_to_value(selected_path)
        self.on_change = self._handle_change

    def _build_options(self) -> List[ft.dropdown.Option]:
        """カテゴリ一覧からドロップダウンの選択肢を生成する。"""
        id_map: Dict[str, Category] = {c.id: c for c in self._categories}

        def build_path(cat: Category) -> List[str]:
            path: List[str] = [cat.name]
            current = cat
            while current.parent_id:
                parent: Optional[Category] = id_map.get(current.parent_id)
                if parent is None:
                    break
                path.append(parent.name)
                current = parent
            return list(reversed(path))

        options: List[ft.dropdown.Option] = []
        for cat in self._categories:
            path_parts = build_path(cat)
            display = " > ".join(path_parts)
            value = self._path_to_value(path_parts)
            # Dropdown Option には value 引数は存在しないため key に統一
            options.append(ft.dropdown.Option(text=display, key=value))
        return options

    def _path_to_value(self, path: List[str]) -> str:
        """パスリストをドロップダウン値（文字列）に変換する。"""
        return " > ".join(path)

    def _handle_change(self, e: ft.ControlEvent) -> None:
        """選択変更時に親へ階層リストを通知する。"""
        raw_value = e.control.value if e.control else ""
        path_list = [part.strip() for part in str(raw_value).split(">") if part.strip()]
        self._on_change(path_list)

    def build(self) -> ft.Dropdown:  # type: ignore[override]
        """Flet ビルド関数。"""
        return self
