import pytest

@pytest.fixture
def service():
    from sqlite_storage import SQLiteStorage
    from items_store import ItemStore
    from items_service import ItemService

    storage = SQLiteStorage(":memory:")
    store = ItemStore(storage)
    return ItemService(store, "test_user")