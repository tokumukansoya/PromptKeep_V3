import pytest
from datetime import datetime

from services.prompt_service import PromptService
from models.prompt import Prompt
from models.app_state import AppState


class DummyDataService:
    pass


def test_create_prompt_default_categories():
    ps = PromptService(DummyDataService())
    p = ps.create_prompt("title", "body")
    assert isinstance(p, Prompt)
    assert p.title == "title"
    assert p.body == "body"
    assert p.category_ids == []


def test_update_prompt_and_categories():
    ps = PromptService(DummyDataService())
    state = AppState.empty()
    prompt = ps.create_prompt("t", "b")
    state.prompts.append(prompt)

    # update categories
    ps.update_prompt(state, prompt.id, category_ids=["cat1", "cat2"])
    updated = ps.get_prompt(state, prompt.id)
    assert updated.category_ids == ["cat1", "cat2"]


def test_delete_and_restore_prompt():
    ps = PromptService(DummyDataService())
    state = AppState.empty()
    prompt = ps.create_prompt("t", "b")
    state.prompts.append(prompt)

    ps.delete_prompt(state, prompt.id)
    assert prompt.deleted_at is not None
    assert prompt.id in state.trash

    ps.restore_prompt(state, prompt.id)
    assert prompt.deleted_at is None
    assert prompt.id not in state.trash
