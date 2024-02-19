import missil
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse

from src.controller.auth import AuthController
from models.user_models import UserLogin, UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

auth = AuthController()

bearer = missil.FlexibleTokenBearer(auth.token_key, auth.token_secret)
rules = missil.make_rules(bearer, "admin", "user")

@router.post("/login")
async def login(user_data: UserLogin):    
    if user_data:
        email = user_data.email
        password = user_data.password

    response = await auth.authenticate_user(email, password)
    
    if response["success"]:
        return JSONResponse(content={
            "success": True,
            "detail": "access-granted",
            "user_data": response["user_data"],
            "token": response["token"]
        }, status_code=200)
    
    raise HTTPException(status_code=401, detail="Invalid email or password")
    


# @router.post("/register", dependencies=[rules["admin"]])
# def register(username: str, password: str):
#     # Your registration logic here
#     return {"message": "Registered successfully"}
