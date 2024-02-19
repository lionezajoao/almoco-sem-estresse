import os
import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext
from src.utils import Utils
from src.lib.user import User
from datetime import datetime, timedelta

load_dotenv()

class Auth:
    def __init__(self):
        self.user = User()
        self.utils = Utils()
        self.token_key = os.environ.get("TOKEN_KEY")
        self.token_secret = os.environ.get("SECRET_KEY")
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def hash_password(self, pwd: str) -> str:
        return self.pwd_context.hash(pwd)
    
    async def get_user_auth(self, email: str, password: str):
        user_data = self.user.get_user_by_email(email)
        
        if not user_data:
            return {
                "success": False,
                "status_code": 404,
                "detail": "user-not-found"
            }
        
        user_data = user_data[0]
        
        hashed_pwd = self.user.get_encrypted_pass(email)
        if not self.verify_password(password, hashed_pwd):
            return {
                "success": False,
                "status_code": 401,
                "detail": "invalid-password"
            }
        
        # Generate JWT token
        payload = {
            "email": email,
            "exp": (datetime.utcnow() + timedelta(hours=12)).isoformat()  # Convert datetime to string
        }
        token = jwt.encode(payload, self.token_secret, algorithm="HS256")
        print(token)
        
        return {
            "success": True,
            "detail": "access-granted",
            "user_data": {
                "name": user_data[1],
                "email": user_data[0],
            },
            "token": token
        }
    
    def verify_token(self, token):
        try:
            decoded_token = self.instance.decode(token, self.token_secret, algorithms=["HS256"])
            return decoded_token.get("key") == self.token_key
        except jwt.exceptions.JWSDecodeError:
            print("JWSEncodeError")
            return False
        except jwt.exceptions.InvalidKeyTypeError:
            return False
        except jwt.exceptions.InvalidTokenError:
            return False
        
    