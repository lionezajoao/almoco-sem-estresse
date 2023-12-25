from database.base import Database

class UserDatabase(Database):
    def __init__(self):
        super().__init__()

    def get_user(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        params = (username,)
        return self.query(query, params)
    
