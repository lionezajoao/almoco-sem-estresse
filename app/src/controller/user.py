from fastapi import HTTPException
from fastapi.responses import JSONResponse

from src.utils import Utils
from src.lib.user import User
from src.database.user import UserDatabase

class UserController:
    def __init__(self):
        self.user = User()
        self.utils = Utils()

    def return_all_users(self):
        return JSONResponse(content=self.user.get_all_users(), status_code=200)
    
    def handle_user(self, email):
        data = self.user.get_user(email)
        if data:
            return JSONResponse(content=data, status_code=200)
        raise HTTPException(status_code=404, detail="User not found")
    
    def handle_user_password(self, email):
        data = self.user.get_user_password(email)
        if data:
            return JSONResponse(content=data, status_code=200)
        raise HTTPException(status_code=404, detail="User not found")
    
    def handle_new_user(self, data):
        user_check = self.user.get_user(data.email)
        if user_check:
            raise HTTPException(status_code=400, detail="User already exists")
        
        hashed_password = self.utils.hash_password(data.password)
        self.insert_user(data.name, data.email, hashed_password, data.role, data.name)
        return JSONResponse(content={"message": "User added successfully"}, status_code=200)
    
    def handle_new_password(self, data):
        if self.user.get_user(data.email):
            new_password = self.utils.hash_password(data.password)
            self.update_user_password(data.name, new_password)
            return JSONResponse(content={"message": "Password updated successfully"}, status_code=200)
        raise HTTPException(status_code=404, detail="User not found")
