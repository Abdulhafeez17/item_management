from items_service import ItemService
from items_store import ItemStore
from sqlite_storage import SQLiteStorage
from auth_repository import AuthRepository
from config import Config


# def init_service():
#     user = input("Enter username: ").strip()  
#     if not user:
#         raise Exception("Authentication required")

#     storage = SQLiteStorage()
#     store = ItemStore(storage)
#     service = ItemService(store, user)   

#     return service
def init_service():

    storage = SQLiteStorage(Config.DATABASE_NAME)

    auth_repo = AuthRepository(storage)

    print("""
=========================
        AUTH MENU
=========================
1. Signup
2. Login
""")

    choice = input("Choose option: ")

    if choice == "1":

        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        try:
            auth_repo.create_user(username, password)

            print("\n✔ Signup successful")
            print("Please login now.\n")

        except Exception as e:
            print(f"Error: {e}")
            return init_service()

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = auth_repo.login_user(username, password)

    if not user:
        print("Invalid username or password")
        return init_service()

    print(f"\n✔ Welcome {user['username']}")

    store = ItemStore(storage)

    service = ItemService(
        store,
        user["username"]
    )

    return service


def print_item(item):
    print(f"""
ID: {item.id}
Title: {item.title}
Description: {item.description}
Priority: {item.priority}
State: {item.state}
Owner: {item.owner}
Created At: {item.created_at}
Updated At: {item.updated_at}
""")


def print_items(items):
    print("\n===== ITEM LIST =====")
    if not items:
        print("No items found.")
        return

    for item in items:
        print(f"[{item.id}] {item.title} | {item.state} | Priority: {item.priority} | Owner: {item.owner}")



def create_item(service):
    print("\n--- CREATE ITEM ---")
    title = input("Title: ")
    description = input("Description: ")
    priority = int(input("Priority (1-5): "))

    try:
        item = service.create_item(title, description, priority)
        print("\n✔ Item created successfully!")
        print_item(item)
    except Exception as e:
        print(f" Error: {e}")


def list_items(service):
    items = service.list_items()
    print_items(items)


def view_item(service):
    item_id = int(input("Enter Item ID: "))

    try:
        item = service.get_item(item_id)
        print_item(item)
    except Exception as e:
        print(f" Error: {e}")


def update_item(service):
    print("\n--- UPDATE ITEM ---")
    item_id = int(input("Enter Item ID: "))

    try:
        item = service.get_item(item_id)

        print("Leave blank to keep current value")

        title = input(f"Title ({item.title}): ") or item.title
        description = input(f"Description ({item.description}): ") or item.description
        priority_input = input(f"Priority ({item.priority}): ")

        priority = int(priority_input) if priority_input else item.priority

        updated = service.update_item(item_id, title, description, priority)

        print("\n✔ Item updated successfully")
        print_item(updated)

    except Exception as e:
        print(f" Error: {e}")


def workflow_menu(service):
    print("\n--- WORKFLOW ACTIONS ---")
    item_id = int(input("Enter Item ID: "))

    print("""
1. Activate
2. Complete
3. Block
4. Reopen
5. Archive
""")

    choice = input("Choose action: ")

    try:
        if choice == "1":
            service.activate_item(item_id)
        elif choice == "2":
            service.complete_item(item_id)
        elif choice == "3":
            service.block_item(item_id)
        elif choice == "4":
            service.reopen_item(item_id)
        elif choice == "5":
            service.archive_item(item_id)   
        else:
            print("Invalid choice")
            return

        print("✔ Workflow updated successfully")

    except Exception as e:
        print(f" Error: {e}")


# ----------------------------
# MAIN MENU LOOP
# ----------------------------
def main():
    service = init_service()

    while True:
        print("""
=========================
      ITEM SYSTEM
=========================
1. List Items
2. View Item
3. Create Item
4. Update Item
5. Workflow Actions
6. Exit
""")

        choice = input("Enter choice: ")

        if choice == "1":
            list_items(service)

        elif choice == "2":
            view_item(service)

        elif choice == "3":
            create_item(service)

        elif choice == "4":
            update_item(service)

        elif choice == "5":
            workflow_menu(service)

        elif choice == "6":
            print("Goodbye ")
            break

        else:
            print("Invalid choice")

        input("\nPress Enter to continue...")



if __name__ == "__main__":
    main()