import pytest
from ui.components.card.card_body import CardBody
from ui.components.card.card_header import CardHeader
from ui.components.card.prompt_card import PromptCard

def test_card_body_render():
    body = CardBody("Test Title", "Test Preview")
    rendered = body.render()
    assert rendered["title"] == "Test Title"
    assert rendered["preview"] == "Test Preview"
    assert "style" in rendered

def test_card_header_render():
    header = CardHeader("Test Header")
    rendered = header.render()
    assert rendered["title"] == "Test Header"
    assert "style" in rendered

def test_prompt_card_render():
    card = PromptCard("Test Title", "Test Preview")
    rendered = card.render()
    assert "header" in rendered
    assert "body" in rendered
    assert rendered["header"]["title"] == "Test Title"
    assert rendered["body"]["preview"] == "Test Preview"