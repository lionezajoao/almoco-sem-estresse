import missil
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import JSONResponse

from app.src.controller.auth import AuthController
from app.models.auth_models import HotmartModel
from app.models.user_models import UserLogin, UserBase

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

@router.get("/verify_code")
def check_code(code: str = Header(...)):
    return JSONResponse(content=auth.check_code(code))

@router.post("/send_password_reset")
async def password_reset(data: UserBase):
    response = await auth.send_password_reset(data.email)
    return JSONResponse(content=response, status_code=response.get("status_code"))

@router.post("/reset_password")
async def reset_password(data: UserLogin, code: str = Header(...)):
    if not auth.check_code(code):
        raise HTTPException(status_code=401, detail="Invalid code")
    response = await auth.reset_password(data.email, data.password)
    return JSONResponse(content=response, status_code=response.get("status_code"))

@router.post("/email_confirmation")
async def email_confirmation(data: UserBase):
    response = await auth.confirm_email(data.email)
    return JSONResponse(content=response, status_code=response.get("status_code"))

