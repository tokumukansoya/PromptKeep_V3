from models.category import Category


def test_category_create_and_dict_roundtrip():
    c = Category.create("work", order=1)
    d = c.to_dict()
    assert d["name"] == "work"
    assert d["order"] == 1

    # simulate old dict that contains parent_id (should be ignored)
    old = {"id": c.id, "name": "work", "parent_id": None, "order": 1}
    parsed = Category.from_dict(old)
    assert parsed.id == c.id
    assert parsed.name == "work"
    assert parsed.order == 1
