from fastapi import Header, HTTPException
from fastapi.responses import JSONResponse

from src.utils import Utils
from src.lib.user import User

class AuthController:
    def __init__(self):
        self.user = User()
        self.utils = Utils()
        pass
    
    async def authenticate_user(self, email: str = Header(...), password: str = Header(...)):
        user_data = self.user.get_user_by_email(email)
        
        if not user_data:
            raise HTTPException(status_code=404, detail="user-not-found")
        
        hashed_pwd = self.user.get_encrypted_pass(email)
        if not self.utils.verify_password(password, hashed_pwd):
            raise HTTPException(status_code=401, detail="invalid-credentials")
        
        return JSONResponse(status_code=200, content={
            "success": True,
            "detail": "access-granted",
            "user_data": {
                "name": user_data[1],
                "email": user_data[0],
            }
        })
