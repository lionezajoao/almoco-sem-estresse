from src.database.user import UserDatabase

class User(UserDatabase):
    def __init__(self):
        super().__init__()

    def get_all_users(self):
        return self.get_users()
    
    def get_user_by_email(self, email):
        return self.get_user(email)[0]
    
    def insert_new_user(self, name, email, password, role):
        return self.insert_user(name, email, password, role)
    
    def get_encrypted_pass(self, email):
        return self.get_user_password(email)[0][0]
    
    def update_user_password(self, email, password):
        return self.update_user_password(email, password)

    def delete_user_by_email(self, email):
        return self.delete_user_by_email(email)