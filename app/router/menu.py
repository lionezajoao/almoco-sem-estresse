from typing import List, Optional
from fastapi import APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.src.controller.auth import AuthController
from app.src.controller.menu import MenuController

from app.models.user_models import UserLogin
from app.models.menu_models import NewMenuModel, MenuItemIngredientsModel

router = APIRouter(
    prefix="/menu",
    tags=["menu"],
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"}
    },
)

menu = MenuController()
auth = AuthController()

@router.get("/get_all_items")
def get_menu(user: UserLogin = Depends(auth.get_current_user)):
    return menu.handle_all_items()

@router.get("/get_item_by_type")
def get_item_by_type(type: str, user: UserLogin = Depends(auth.get_current_user)):
    return menu.handle_data_by_type(type)

@router.get("/get_all_ingredients")
def get_ingredients(user: UserLogin = Depends(auth.get_current_user)):
    return menu.handle_all_ingredients()

@router.get("/get_item")
def get_item_by_name(name: str, user: UserLogin = Depends(auth.get_current_user)):
    return menu.handle_data_by_name(name)

@router.get("/get_ingredients")
def get_ingredients_by_name(name: str, user: UserLogin = Depends(auth.get_current_user)):
    return menu.handle_ingredients_by_name(name)

@router.get("/get_item_ingredients")
def get_ingredients(name: str, user: UserLogin = Depends(auth.get_current_user)):
    return menu.handle_ingredients_from_item(name)

@router.post("/add_new_item")
def add_new_item(request: MenuItemIngredientsModel, token_data: UserLogin = Depends(auth.get_current_user)):
    return menu.handle_insert_new_item(request, token_data)

@router.post("/create_menu")
def create_menu(request: NewMenuModel, token_data: dict = Depends(auth.get_current_user)):
    return menu.handle_create_menu(request, token_data)