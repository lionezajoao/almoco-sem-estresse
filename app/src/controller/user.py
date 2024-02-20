from fastapi import HTTPException
from fastapi.responses import JSONResponse

from src.lib.auth import Auth
from src.lib.user import User
from app.src.lib.email_sender import EmailSender

class UserController:
    def __init__(self):
        self.user = User()
        self.auth = Auth()
        self.email = EmailSender()
        self.scope = ["admin"]

    def return_all_users(self, token_data):
        if self.user.verify_user_role(token_data.get("email"), token_data.get("role"), self.scope):
            return JSONResponse(content=self.user.get_all_users(), status_code=200)
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    def handle_user(self, email, token_data):
        if self.user.verify_user_role(token_data.get("email"), token_data.get("role"), self.scope):
            data = self.user.get_user(email)
            if data:
                return JSONResponse(content=data, status_code=200)
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    def handle_user_password(self, email, token_data):
        if self.user.verify_user_role(token_data.get("email"), token_data.get("role"), self.scope):
            data = self.user.get_user_password(email)
            if data:
                return JSONResponse(content=data, status_code=200)
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    def handle_new_user(self, data, token_data):
        if self.user.verify_user_role(token_data.get("email"), token_data.get("role"), self.scope):
            user_check = self.user.get_user(data.email)
            if user_check:
                raise HTTPException(status_code=400, detail="User already exists")
            
            hashed_password = self.auth.hash_password(data.password)
            self.user.insert_new_user(data.name, data.email, hashed_password, data.role)
            email_msg = f"""
            Olá!
            Seja bem-vindo ao nosso sistema! Sua senha provisória é: { data.password } . Recomendamos que você altere sua senha assim que possível.
            """
            self.email.send_text_email(subject="Senha provisória", recipients=[data.email], body=email_msg)
            return JSONResponse(content={ "success": True, "message": "User added successfully"}, status_code=200)
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    def handle_new_password(self, data, token_data):
        if self.user.verify_user_role(token_data.get("email"), token_data.get("role"), self.scope):
            if self.user.get_user(data.email):
                new_password = self.auth.hash_password(data.password)
                self.update_user_password(data.name, new_password)
                return JSONResponse(content={"message": "Password updated successfully"}, status_code=200)
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=401, detail="Unauthorized")
