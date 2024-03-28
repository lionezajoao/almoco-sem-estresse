from fastapi import Header, HTTPException
from fastapi.responses import JSONResponse

from app.src.lib.auth import Auth
from app.models.user_models import UserLogin

class AuthController(Auth):
    def __init__(self):
        super().__init__()
    
    async def authenticate_user(self, user_data: UserLogin):
        if not user_data:
            return JSONResponse(status_code=400, content={"detail": "Invalid data"})
        
        email = user_data.email
        password = user_data.password
        return await self.get_user_auth(email, password)
    
    async def get_current_user(self, token: str = Header(...)):
        data = self.verify_token(token)
        if data.get("success") is False:
            raise HTTPException(status_code=401, detail="Invalid token")
        return data
    
    async def confirm_email(self, email: str):
        return await self.send_email_confirmation(email)

    async def send_password_reset(self, email: str):
        return await self.send_reset_password_email(email)

    def check_code(self, code: str):
        return self.verify_code(code)
    
    def check_hotmart_token(self, x_hotmart_hottok: str = Header(...)):
        if not self.verify_hotmart_token(x_hotmart_hottok):
            raise HTTPException(status_code=401, detail="Invalid token")
    
    async def reset_password(self, email: str, password: str):
        return await self.change_password(email, password)
