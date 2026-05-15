# def test_create_and_list(service):
#     service.create_item("A", "B", 1)
#     items = service.list_items()
#     assert len(items) == 1

# def test_update(service):
#     item = service.create_item("A", "B", 1)
#     updated = service.update_item(item.id, "X", "Y", 2)
#     assert updated.title == "X"

# def test_delete(service):
#     item = service.create_item("A", "B", 1)
#     service.delete_item(item.id)
#     assert service.list_items() == []