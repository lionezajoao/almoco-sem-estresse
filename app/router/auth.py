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
async def login(request:Request, data: UserLogin):
    email = data.email
    password = data.password
    user = await auth.authenticate_user(email, password)
    if user:
        return JSONResponse(status_code=200, content={"redirect": "http://localhost:8000/menu"})
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    


@router.post("/register")
def register(username: str, password: str):
    # Your registration logic here
    return {"message": "Registered successfully"}
