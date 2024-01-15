from src.database.user import UserDatabase

class User(UserDatabase):
    def __init__(self):
        super().__init__()

    def get_all_users(self):
        return self.get_users()
    
    def get_user_by_email(self, email):
        return self.get_user(email)
    
    def insert_user(self, email, password):
        return self.insert_user(email, password)
    
    def update_user_password(self, email, password):
        return self.update_user_password(email, password)

    def delete_user_by_email(self, email):
        return self.delete_user_by_email(email)