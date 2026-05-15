from item import Item

class ItemStore:
    def __init__(self, storage):
        self.storage = storage

    def add(self, item):
        try:
            self.storage.execute("BEGIN")

            cursor = self.storage.execute("""
            INSERT INTO items (title, description, created_at, priority, state, owner)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item.title,
                item.description,
                item.created_at.isoformat(),
                item.priority,
                item.state,
                item.owner
            ))

            item.id = cursor.lastrowid

            self.storage.execute("""
            INSERT INTO item_activity (item_id, action)
            VALUES (?, ?)
            """, (item.id, "created"))

            self.storage.commit()

        except:
            self.storage.rollback()
            raise

    def get_all(self, owner):
        rows = self.storage.fetch_all("""
        SELECT * FROM items
        WHERE owner = ?
        ORDER BY priority DESC, created_at DESC
        """, (owner,))
        return [Item.from_dict(dict(r)) for r in rows]

    def find_by_id(self, item_id, owner):
        row = self.storage.fetch_one(
            "SELECT * FROM items WHERE id = ? AND owner = ?",
            (item_id, owner)
        )
        return Item.from_dict(dict(row)) if row else None

    def update(self, item):
        try:
            self.storage.execute("BEGIN")

            self.storage.execute("""
            UPDATE items
            SET title=?, description=?, updated_at=?, priority=?, state=?
            WHERE id=? AND owner=?
            """, (
                item.title,
                item.description,
                item.updated_at.isoformat() if item.updated_at else None,
                item.priority,
                item.state,
                item.id,
                item.owner
            ))

            self.storage.execute("""
            INSERT INTO item_activity (item_id, action)
            VALUES (?, ?)
            """, (item.id, "updated"))

            self.storage.commit()

        except:
            self.storage.rollback()
            raise

    def remove(self, item, owner):
        try:
            self.storage.execute("BEGIN")

            self.storage.execute("""
            INSERT INTO item_activity (item_id, action)
            VALUES (?, ?)
            """, (item.id, "deleted"))

            self.storage.execute(
                "DELETE FROM items WHERE id = ? AND owner = ?",
                (item.id, owner)
            )

            self.storage.commit()

        except:
            self.storage.rollback()
            raise

    def log_state_change(self, item_id, from_state, to_state, action):
        self.storage.execute("""
        INSERT INTO item_activity (item_id, action)
        VALUES (?, ?)
        """, (item_id, f"{action}: {from_state} → {to_state}"))
        self.storage.commit()

    def get_by_state(self, state, owner):
        rows = self.storage.fetch_all(
            "SELECT * FROM items WHERE state=? AND owner=? ORDER BY priority DESC, created_at DESC",
            (state, owner)
        )
        return [Item.from_dict(dict(r)) for r in rows]

    def get_summary(self, owner):
        rows = self.storage.fetch_all("""
        SELECT state, COUNT(*) as count
        FROM items
        WHERE owner=?
        GROUP BY state
        """, (owner,))
        return {row["state"]: row["count"] for row in rows}

    def search_by_title(self, keyword, owner):
        rows = self.storage.fetch_all("""
        SELECT * FROM items
        WHERE title LIKE ? AND owner=?
        ORDER BY priority DESC, created_at DESC
        """, (f"{keyword}%", owner))
        return [Item.from_dict(dict(r)) for r in rows]

    def get_paginated(self, limit, offset, owner):
        rows = self.storage.fetch_all("""
        SELECT * FROM items
        WHERE owner=?
        ORDER BY priority DESC, created_at DESC
        LIMIT ? OFFSET ?
        """, (owner, limit, offset))
        return [Item.from_dict(dict(r)) for r in rows]

    def search_paginated(self, keyword, limit, offset, owner):
        rows = self.storage.fetch_all("""
        SELECT * FROM items
        WHERE title LIKE ? AND owner=?
        ORDER BY priority DESC, created_at DESC
        LIMIT ? OFFSET ?
        """, (f"{keyword}%", owner, limit, offset))
        return [Item.from_dict(dict(r)) for r in rows]

    def get_activities(self, item_id):
        rows = self.storage.fetch_all("""
        SELECT * FROM item_activity
        WHERE item_id=?
        ORDER BY timestamp DESC
        """, (item_id,))
        return [dict(r) for r in rows]