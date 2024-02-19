from fastapi import Header, HTTPException
from fastapi.responses import JSONResponse

from src.utils import Utils
from src.lib.auth import Auth

class AuthController(Auth):
    def __init__(self):
        super().__init__()
    
    async def authenticate_user(self, email: str, password: str):
        return await self.get_user_auth(email, password)
    
    async def get_current_user(self, token: str = Header(...)):
        return self.verify_token(token)
