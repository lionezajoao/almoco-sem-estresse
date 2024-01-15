from fastapi import APIRouter

from src.controller.user import UserController
from models.user_models import UserLogin, UserCreate

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"}
    },
)
user = UserController()

@router.get("/list_all_users")
def get_users():
    return user.return_all_users()

@router.get("/get_user")
def get_user_by_email(email: str):
    return user.handle_user(email)

@router.get("/get_user_password")
def get_user_password_by_email(email: str):
    return user.handle_user_password(email)

@router.post("/add_new_user")
def add_new_user(request: UserCreate):
    return user.handle_new_user(request)

@router.post("/update_user_password")
def update_user_password(email: str):
    return user.handle_new_password(email)