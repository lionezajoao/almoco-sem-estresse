from fastapi import APIRouter, Depends, Header

from app.src.controller.user import UserController
from app.src.controller.auth import AuthController
from app.models.auth_models import GuruModel
from app.models.user_models import UserBase, UserCreate

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
auth = AuthController()


@router.get("/list_all_users")
def list_all_users(token_data: dict = Depends(auth.get_current_user)):
    return user.return_all_users(token_data)

@router.get("/get_user")
def get_user_by_email(email: str, token_data: dict = Depends(auth.get_current_user)):
    return user.handle_user(email, token_data)

@router.get("/get_user_password")
def get_user_password_by_email(email: str, token_data: dict = Depends(auth.get_current_user)):
    return user.handle_user_password(email, token_data)

@router.post("/create_user")
def add_new_user(request: UserCreate, token_data: dict = Depends(auth.get_current_user)):
    return user.handle_new_user(request, token_data)

@router.delete("/delete_user")
def delete_user_by_email(data: UserBase, token_data: dict = Depends(auth.get_current_user)):
    return user.handle_delete_user(data.email, token_data)

@router.post("/guru_webhook")
def guru_webhook(data: GuruModel, token: bool = Depends(auth.check_guru_token)):
    return user.handle_guru_webhook(data)
