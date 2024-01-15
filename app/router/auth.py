from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse


from models.user_models import UserLogin, UserCreate
from fastapi import Form

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)
@router.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    # Your login logic here
    return {"message": f"Login successful for email: {email, password}"}

@router.post("/register")
def register(username: str, password: str):
    # Your registration logic here
    return {"message": "Registered successfully"}

