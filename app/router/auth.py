from typing import Optional
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

from src.controller.auth import AuthController
from models.user_models import UserLogin, UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

auth = AuthController()

@router.post("/login")
async def login(user_data: UserLogin):    
    if user_data:
        email = user_data.email
        password = user_data.password

    user = await auth.authenticate_user(email, password)
    if user:
        return JSONResponse(content={
            "success": True,
            "detail": "access-granted",
        }, status_code=200)
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    


@router.post("/register")
def register(username: str, password: str):
    # Your registration logic here
    return {"message": "Registered successfully"}
