from models.user import User

class AuthManager:
    """user authentication manager"""

    def __init__(self):
        #users and their roles
        self.users = {}
        self.users["admin"] = User("admin", "admin123", "admin")
        self.users["user"] = User("user", "user123", "user")

    def login(self, username: str, password: str):
        """logging in a user and returning user object if its successful"""
        if username in self.users:
            user = self.users[username]
            if user.verify_password(password):
                return user
        return None

    def register (self, username: str, password: str, role: str = "user"):
        """registering a new user"""
        if username in self.users:
            return False

        self.users[username] = User(username, password, role)
        return True

