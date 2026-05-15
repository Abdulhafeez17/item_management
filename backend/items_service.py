from datetime import datetime
from item import Item
from logger import logger

ALLOWED_TRANSITIONS = {
    "draft": ["active"],
    "active": ["blocked", "completed"],
    "blocked": ["active"],
    "completed": ["archived", "active"],
    "archived": []
}

class ItemService:
    def __init__(self, store, current_user):
        if not current_user:
            raise Exception("Authentication required")

        self.store = store
        self.current_user = current_user

    def create_item(self, title, description, priority=0):
        try:
            item = Item(None, title, description, priority, state="draft", owner=self.current_user)
            self.store.add(item)

            logger.info(f"Item created id={item.id}", extra={"user": self.current_user})
            return item

        except Exception as e:
            logger.error(f"Create failed: {str(e)}", extra={"user": self.current_user})
            raise

    def list_items(self):
        return self.store.get_all(self.current_user)

    def get_item(self, item_id):
        item = self.store.find_by_id(item_id, self.current_user)
        if not item:
            logger.warning(f"Unauthorized access item_id={item_id}", extra={"user": self.current_user})
            raise Exception("Access denied or item not found")
        return item

    def update_item(self, item_id, title=None, description=None, priority=None):
        try:
            item = self.get_item(item_id)
            item.update(title, description, priority)
            item.updated_at = datetime.utcnow()
            self.store.update(item)

            logger.info(f"Item updated id={item_id}", extra={"user": self.current_user})
            return item

        except Exception as e:
            logger.error(f"Update failed id={item_id}: {str(e)}", extra={"user": self.current_user})
            raise

    def delete_item(self, item_id):
        item = self.get_item(item_id)
        self.store.remove(item, self.current_user)

        logger.info(f"Item deleted id={item_id}", extra={"user": self.current_user})
        return True

    def _change_state(self, item, new_state, action):
        if new_state not in ALLOWED_TRANSITIONS[item.state]:
            logger.error(f"Invalid transition {item.state}->{new_state}", extra={"user": self.current_user})
            raise Exception("Invalid transition")

        old_state = item.state
        item.set_state(new_state)

        self.store.update(item)
        self.store.log_state_change(item.id, old_state, new_state, action)

        logger.info(
            f"Workflow {action} id={item.id} {old_state}->{new_state}",
            extra={"user": self.current_user}
        )

    def activate_item(self, item_id):
        self._change_state(self.get_item(item_id), "active", "activate")

    def block_item(self, item_id):
        self._change_state(self.get_item(item_id), "blocked", "block")

    def complete_item(self, item_id):
        self._change_state(self.get_item(item_id), "completed", "complete")

    def reopen_item(self, item_id):
        self._change_state(self.get_item(item_id), "active", "reopen")

    def archive_item(self, item_id):
        self._change_state(self.get_item(item_id), "archived", "archive")

    def get_by_state(self, state):
        return self.store.get_by_state(state, self.current_user)

    def summary(self):
        return self.store.get_summary(self.current_user)

    def search(self, keyword):
        if not keyword:
            return []
        return self.store.search_by_title(keyword, self.current_user)

    def paginate(self, limit, offset):
        return self.store.get_paginated(limit, offset, self.current_user)

    def search_paginated(self, keyword, limit, offset):
        if not keyword:
            return []
        return self.store.search_paginated(keyword, limit, offset, self.current_user)