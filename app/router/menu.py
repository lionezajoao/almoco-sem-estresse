from fastapi import APIRouter

from src.controller.menu import MenuController
from models.menu_models import MenuItemModel, IngredientsModel, MenuItemIngredientsModel

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


@router.get("/list_all_items")
def get_menu():
    return menu.handle_all_items()

@router.get("/get_item_by_type")
def get_item_by_type(type: str):
    return menu.handle_data_by_type(type)

@router.get("/list_all_ingredients")
def get_ingredients():
    return menu.handle_all_ingredients()

@router.get("/get_item")
def get_item_by_name(name: str):
    return menu.handle_data_by_name(name)

@router.get("/get_ingredients")
def get_ingredients_by_name(name: str):
    return menu.handle_ingredients_by_name(name)

@router.get("/get_item_ingredients")
def get_ingredients(name: str):
    return menu.handle_ingredients_from_item(name)

@router.post("/add_new_item")
def add_new_item(request: MenuItemIngredientsModel):
    return menu.handle_insert_new_item(request)