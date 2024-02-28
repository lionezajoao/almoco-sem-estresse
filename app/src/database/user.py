import uuid
from app.src.database.base import Database

class UserDatabase(Database):
    def __init__(self):
        super().__init__()

    def get_users(self):
        query = "SELECT email, name, role FROM users"
        return self.query(query)

    def get_user(self, email):
        query = "SELECT email, name, role FROM users WHERE email = %s"
        params = (email,)
        return self.query(query, params)
    
    def get_user_password(self, email):
        query = "SELECT password FROM users WHERE email = %s"
        params = (email,)
        return self.query(query, params)
    
    def insert_user(self, name, email, password, role):
        user_id = str(uuid.uuid4())
        query = "INSERT INTO users (_id, email, password, role, name) VALUES (%s, %s, %s, %s, %s)"
        params = (user_id, email, password, role, name)
        return self.insert(query, params)
    
    def update_user_password(self, email, password):
        query = "UPDATE users SET password = %s WHERE email = %s"
        params = (password, email)
        return self.query(query, params)

    def delete_user_by_email(self, email):
        query = "DELETE FROM users WHERE email = %s;"
        params = (email,)
        self.delete(query, params)
