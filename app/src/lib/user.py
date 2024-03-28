from app.src.database.user import UserDatabase

class User(UserDatabase):
    def __init__(self):
        super().__init__()

    def get_all_users(self):
        self.connect()
        result = self.get_users()
        self.close()
        return result
    
    def get_user_by_email(self, email):
        self.connect()
        result = self.get_user(email)
        self.close()
        return result
    
    def insert_new_user(self, name, email, password, role):
        self.connect()
        result = self.insert_user(name, email, password, role)
        self.close()
        return result
    
    def get_encrypted_pass(self, email):
        self.connect()
        result = self.get_user_password(email)[0][0]
        self.close()
        return result
    
    def update_password(self, email, password):
        self.connect()
        result = self.update_user_password(email, password)
        self.close()
        return result

    def delete_user(self, email):
        self.connect()
        result = self.delete_user_by_email(email)
        self.close()
        return result
    
    def verify_user_role(self, email: str, role: str, allowed_roles: list) -> bool:
        self.connect()
        user_data = self.get_user(email)
        self.close()
        if not user_data:
            return False
        
        user_role = user_data[0][2]

        if user_role != role:
            return False

        if user_role not in allowed_roles:
            return False
        
        return role in allowed_roles
    