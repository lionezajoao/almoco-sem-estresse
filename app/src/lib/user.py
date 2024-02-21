from src.database.user import UserDatabase

class User(UserDatabase):
    def __init__(self):
        super().__init__()

    def get_all_users(self):
        return self.get_users()
    
    def get_user_by_email(self, email):
        return self.get_user(email)
    
    def insert_new_user(self, name, email, password, role):
        return self.insert_user(name, email, password, role)
    
    def get_encrypted_pass(self, email):
        return self.get_user_password(email)[0][0]
    
    def update_password(self, email, password):
        return self.update_user_password(email, password)

    def delete_user(self, email):
        return self.delete_user_by_email(email)
    
    def verify_user_role(self, email: str, role: str, allowed_roles: list) -> bool:
        user_data = self.get_user(email)
        if not user_data:
            return False
        
        user_role = user_data[0][2]

        if user_role != role:
            return False

        if user_role not in allowed_roles:
            return False
        
        return role in allowed_roles
    