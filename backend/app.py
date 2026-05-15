from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlite_storage import SQLiteStorage
from items_store import ItemStore
from items_service import ItemService
from config import Config
from auth_repository import AuthRepository


# app = Flask(__name__)
# CORS(app)
# storage = SQLiteStorage(Config.DATABASE_NAME)
# store = ItemStore(storage)


# # HELPER
# def get_service():
#     user = request.headers.get("X-User")

#     if not user:
#         return None

#     return ItemService(store, user)

app = Flask(__name__)
CORS(app)

storage = SQLiteStorage(Config.DATABASE_NAME)

store = ItemStore(storage)

auth_repo = AuthRepository(storage)


def get_service():

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    token = auth_header.split(" ")[1]

    return ItemService(store, token)

@app.route("/signup", methods=["POST"])
def signup():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    try:
        auth_repo.create_user(username, password)

        return jsonify({
            "message": "User created successfully"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    user = auth_repo.login_user(username, password)

    if not user:
        return jsonify({
            "error": "Invalid credentials"
        }), 401

    return jsonify({
        "token": user["username"],
        "user": user
    })


@app.route("/logout", methods=["POST"])
def logout():

    return jsonify({
        "message": "Logout successful"
    }), 200


@app.route("/profile")
def profile():

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    token = auth_header.split(" ")[1]

    return jsonify({
        "logged_in_user": token
    })



# HOME
@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "Flask API Running"
    })



# CREATE ITEM
@app.route("/items", methods=["POST"])
def create_item():
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    data = request.json

    if not data:
        return jsonify({
            "error": "Invalid JSON"
        }), 400

    try:
        item = service.create_item(
            title=data.get("title"),
            description=data.get("description"),
            priority=data.get("priority", 0)
        )

        return jsonify({
            "success": True,
            "data": item.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# GET ALL ITEMS
# GET /items
@app.route("/items", methods=["GET"])
def get_items():
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    items = service.list_items()

    return jsonify({
        "success": True,
        "data": [item.to_dict() for item in items]
    })



# GET SINGLE ITEM
# GET /items/<id>

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    try:
        item = service.get_item(item_id)

        return jsonify({
            "success": True,
            "data": item.to_dict()
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 404



# UPDATE ITEM
# PUT /items/<id>

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    data = request.json

    if not data:
        return jsonify({
            "error": "Invalid JSON"
        }), 400

    try:
        item = service.update_item(
            item_id,
            title=data.get("title"),
            description=data.get("description"),
            priority=data.get("priority")
        )

        return jsonify({
            "success": True,
            "data": item.to_dict()
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400



# DELETE ITEM
# DELETE /items/<id>

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    try:
        service.delete_item(item_id)

        return jsonify({
            "success": True,
            "message": "Item deleted"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400



# ACTIVATE ITEM
# POST /items/<id>/activate

@app.route("/items/<int:item_id>/activate", methods=["POST"])
def activate_item(item_id):
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    try:
        service.activate_item(item_id)

        return jsonify({
            "success": True,
            "message": "Item activated"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# --------------------------------
# BLOCK ITEM
# POST /items/<id>/block
# --------------------------------
@app.route("/items/<int:item_id>/block", methods=["POST"])
def block_item(item_id):
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    try:
        service.block_item(item_id)

        return jsonify({
            "success": True,
            "message": "Item blocked"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400



# POST /items/<id>/complete

@app.route("/items/<int:item_id>/complete", methods=["POST"])
def complete_item(item_id):
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    try:
        service.complete_item(item_id)

        return jsonify({
            "success": True,
            "message": "Item completed"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400



# REOPEN ITEM


@app.route("/items/<int:item_id>/reopen", methods=["POST"])
def reopen_item(item_id):
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    try:
        service.reopen_item(item_id)

        return jsonify({
            "success": True,
            "message": "Item reopened"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# ARCHIVE ITEM
# POST /items/<id>/archive

@app.route("/items/<int:item_id>/archive", methods=["POST"])
def archive_item(item_id):
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    try:
        service.archive_item(item_id)

        return jsonify({
            "success": True,
            "message": "Item archived"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400



# FILTER BY STATE
# GET /items/state/active

@app.route("/items/state/<state>", methods=["GET"])
def get_items_by_state(state):
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    try:
        items = service.get_by_state(state)

        return jsonify({
            "success": True,
            "data": [item.to_dict() for item in items]
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400



# SEARCH ITEMS
# GET /items/search?q=test

@app.route("/items/search", methods=["GET"])
def search_items():
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    keyword = request.args.get("q", "")

    items = service.search(keyword)

    return jsonify({
        "success": True,
        "data": [item.to_dict() for item in items]
    })


# PAGINATED ITEMS
# GET /items/paginate?limit=5&offset=0

@app.route("/items/paginate", methods=["GET"])
def paginate_items():
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))

    items = service.paginate(limit, offset)

    return jsonify({
        "success": True,
        "data": [item.to_dict() for item in items]
    })


# --------------------------------
# SEARCH + PAGINATION
# GET /items/search/paginated?q=test&limit=5&offset=0
# --------------------------------
@app.route("/items/search/paginated", methods=["GET"])
def search_paginated():
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    keyword = request.args.get("q", "")
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))

    items = service.search_paginated(keyword, limit, offset)

    return jsonify({
        "success": True,
        "data": [item.to_dict() for item in items]
    })



# SUMMARY
# GET /summary

@app.route("/summary", methods=["GET"])
def summary():
    service = get_service()

    if not service:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    return jsonify({
        "success": True,
        "data": service.summary()
    })

# START SERVER

if __name__ == "__main__":
    app.run(debug=Config.DEBUG)