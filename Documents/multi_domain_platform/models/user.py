import hashlib

class User:
    def __init__(self, username: str, password: str, role: str):
        self._username = username
        self._password_hash = self._hash_password(password)
        self._role = role

    def get_username(self) -> str:
        return self._username

    def get_role(self) -> str:
        return self._role

    def is_admin(self) -> bool:
        return self._role.lower() == "admin"

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        """Verify password by comparing hashes."""
        input_hash = self._hash_password(password)
        return self._password_hash == input_hash

    def __str__(self):
        return f"User({self._username}, role={self._role})"