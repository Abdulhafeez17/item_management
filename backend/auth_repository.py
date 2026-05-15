from werkzeug.security import generate_password_hash, check_password_hash

class AuthRepository:

    def __init__(self, storage):
        self.storage = storage

    def create_user(self, username, password):

        hashed_password = generate_password_hash( password, method='pbkdf2:sha256')
        self.storage.conn.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, hashed_password)
        )

        self.storage.conn.commit()

    def login_user(self, username, password):

        user = self.storage.conn.execute(
            """
            SELECT * FROM users
            WHERE username=?
            """,
            (username,)
        ).fetchone()

        if not user:
            return None

        if not check_password_hash(user["password"], password):
            return None

        return {
            "id": user["id"],
            "username": user["username"]
        }