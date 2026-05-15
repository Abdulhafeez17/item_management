import pytest
from item import Item

def test_valid_item():
    item = Item(1, "Test", "Desc", owner="user")
    assert item.title == "Test"

def test_invalid_title():
    with pytest.raises(ValueError):
        Item(1, "", "Desc", owner="user")

def test_invalid_owner():
    with pytest.raises(ValueError):
        Item(1, "Test", "Desc", owner="")

def test_valid_transition():
    item = Item(1, "A", "B", owner="user")
    item.set_state("active")
    assert item.state == "active"

def test_invalid_state():
    item = Item(1, "A", "B", owner="user")
    with pytest.raises(ValueError):
        item.set_state("wrong")