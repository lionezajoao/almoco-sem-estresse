import missil
from fastapi import APIRouter, HTTPException, Depends
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
    response = await auth.authenticate_user(user_data)
    
    if response["success"]:
        return JSONResponse(content={
            "success": True,
            "detail": "access-granted",
            "user_data": response["user_data"],
            "token": response["token"]
        }, status_code=200)
    
    raise HTTPException(status_code=401, detail="Invalid email or password")
    
@router.get("/verify_token")
def verify_token(token_data: dict = Depends(auth.get_current_user)):
    if token_data.get("success") is False:
        raise HTTPException(status_code=401, detail="Invalid token")
    return JSONResponse(content=token_data, status_code=200)

@router.post("/register", dependencies=[rules["admin"].WRITE])
def register(username: str, password: str):
    # Your registration logic here
    return {"message": "Registered successfully"}
