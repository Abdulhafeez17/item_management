import pytest
from items_service import ItemService

def test_create_item(service):
    item = service.create_item("A", "B", 1)
    assert item.owner == "test_user"

def test_create_and_list(service):
    service.create_item("A", "B", 1)
    items = service.list_items()
    assert len(items) == 1

def test_update(service):
    item = service.create_item("A", "B", 1)
    updated = service.update_item(item.id, "X", "Y", 2)
    assert updated.title == "X"

def test_delete(service):
    item = service.create_item("A", "B", 1)
    service.delete_item(item.id)
    assert service.list_items() == []

def test_access_control(service):
    item = service.create_item("A", "B", 1)

    other = ItemService(service.store, "other")

    with pytest.raises(Exception):
        other.get_item(item.id)