from datetime import datetime

VALID_STATES = ["draft", "active", "blocked", "completed", "archived"]

class Item:
    def __init__(self, id, title, description, priority=0,
                 state="draft", owner=None, created_at=None, updated_at=None):

        self._validate_id(id)
        self._validate_title(title)
        self._validate_description(description)
        self._validate_priority(priority)
        self._validate_state(state)
        self._validate_owner(owner)

        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at

        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.state = state
        self.owner = owner

    def _validate_id(self, id):
        if id is not None and (not isinstance(id, int) or id <= 0):
            raise ValueError("Invalid ID")

    def _validate_title(self, title):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Invalid title")

    def _validate_description(self, description):
        if description is not None and not isinstance(description, str):
            raise ValueError("Invalid description")

    def _validate_priority(self, priority):
        if not isinstance(priority, int):
            raise ValueError("Invalid priority")

    def _validate_state(self, state):
        if state not in VALID_STATES:
            raise ValueError(f"Invalid state: {state}")

    def _validate_owner(self, owner):
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Invalid owner")

    def set_state(self, new_state):
        self._validate_state(new_state)
        self.state = new_state
        self.updated_at = datetime.utcnow()

    
    def rename(self, title):
        self._validate_title(title)
        if title != self.title:
            self.title = title
            return True
        return False

    def update_description(self, description):
        self._validate_description(description)
        if description != self.description:
            self.description = description
            return True
        return False
    

    def update_priority(self, priority):
        self._validate_priority(priority)
        if priority != self.priority:
            self.priority = priority
            return True
        return False


   

    def update(self, title=None, description=None, priority=None):
        changed = False

        if title is not None:
            changed = self.rename(title) or changed

        if description is not None:
            changed = self.update_description(description) or changed

        if priority is not None:
            changed = self.update_priority(priority) or changed

        return changed


    def __str__(self):
     return f"{self.title} ({self.state}, priority {self.priority})"


    
    def __repr__(self):
        return (
        f"Item(id={self.id}, title='{self.title}', "
        f"description='{self.description}', priority={self.priority}, "
        f"state='{self.state}', owner='{self.owner}', "
        f"created_at='{self.created_at}', updated_at='{self.updated_at}')"
        )

    

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "state": self.state,
            "owner": self.owner,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data):
        return Item(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            priority=data.get("priority", 0),
            state=data.get("state", "draft"),
            owner=data["owner"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]) if data["updated_at"] else None
        )