import os
import jwt
import bcrypt

from datetime import datetime, timedelta

from app.src.utils import Utils
from app.src.lib.user import User
from app.src.lib.email_sender import EmailSender



class Auth:
    def __init__(self):
        self.user = User()
        self.utils = Utils()
        self.email = EmailSender()
        self.token_key = os.environ.get("TOKEN_KEY")
        self.token_secret = os.environ.get("SECRET_KEY")
        self.hotmart_token = os.environ.get("HOTMART_TOKEN")

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    
    def verify_hotmart_token(self, token: str) -> bool:
        return token == self.hotmart_token
    
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
            "name": user_data[1],
            "role": user_data[2],
            "exp": int((datetime.utcnow() + timedelta(hours=12)).timestamp())  # Convert datetime to integer
        }
        token = jwt.encode(payload, self.token_secret, algorithm="HS256")
        
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
            decoded_token = jwt.decode(token, self.token_secret, algorithms=["HS256"])
            return {
                "success": True,
                "email": decoded_token["email"],
                "name": decoded_token["name"],
                "role": decoded_token["role"]
            }
        except jwt.ExpiredSignatureError:
            return {
                "success": False,
                "status_code": 401,
                "detail": "expired-token"
            }
        except jwt.InvalidTokenError:
            return {
                "success": False,
                "status_code": 401,
                "detail": "invalid-token"
            }
        except Exception as e:
            return {
                "success": False,
                "status_code": 401,
                "detail": f"Something went wrong: {e}"
            }
        
    async def send_email_confirmation(self, email: str):

        user = self.user.get_user_by_email(email)
        if not user:
            return {
                "success": False,
                "status_code": 404,
                "detail": "user-not-found"
            }
        # Generate confirmation token
        confirmation_token = jwt.encode({"email": email}, self.token_secret, algorithm="HS256")
        
        # Send confirmation email
        email_subject = "Confirmação de email"
        email_body = f"Link de confirmação do email: {confirmation_token}"
        self.email.send_text_email(email_subject, [email], email_body)
        return {
            "success": True,
            "status_code": 200,
            "detail": "confirmation-email-sent"
        }
    
    async def send_reset_password_email(self, email: str):
        user = self.user.get_user_by_email(email)
        if not user:
            return {
                "success": False,
                "status_code": 404,
                "detail": "user-not-found"
            }
        # Generate reset password token
        reset_token = jwt.encode({"email": email}, self.token_secret, algorithm="HS256")
        
        # Send reset password email
        email_subject = "Redefinição de senha"
        email_body = f"Código de redefinição de senha: {reset_token}"
        self.email.send_text_email(email_subject, [email], email_body)
        return {
            "success": True,
            "status_code": 200,
            "detail": "reset-password-email-sent"
        }
    
    def verify_code(self, code: str):
        try:
            decoded_token = jwt.decode(code, self.token_secret, algorithms=["HS256"])
            return {
                "success": True,
                "email": decoded_token["email"]
            }
        except jwt.ExpiredSignatureError:
            return {
                "success": False,
                "status_code": 401,
                "detail": "expired-token"
            }
        except jwt.InvalidTokenError:
            return {
                "success": False,
                "status_code": 401,
                "detail": "invalid-token"
            }
        except Exception as e:
            return {
                "success": False,
                "status_code": 401,
                "detail": f"Something went wrong: {e}"
            }
    
    async def change_password(self, email: str, password: str):
        hashed_pwd = self.hash_password(password)
        self.user.update_user_password(email, hashed_pwd)
        return {
            "success": True,
            "status_code": 200,
            "detail": "password-changed"
        }
