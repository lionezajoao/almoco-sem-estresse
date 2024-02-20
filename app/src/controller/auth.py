from fastapi import Header, HTTPException
from fastapi.responses import JSONResponse

from src.utils import Utils
from src.lib.auth import Auth
from models.user_models import UserLogin

class AuthController(Auth):
    def __init__(self):
        super().__init__()
    
    async def authenticate_user(self, user_data: UserLogin):
        if user_data:
            email = user_data.email
            password = user_data.password
        return await self.get_user_auth(email, password)
    
    async def get_current_user(self, token: str = Header(...)):
        data = self.verify_token(token)
        if data.get("success") is False:
            raise HTTPException(status_code=401, detail="Invalid token")
        return data
