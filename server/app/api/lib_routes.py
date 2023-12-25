from fastapi import APIRouter

from lib.menu_lib import MenuLib
from models.menu_models import MenuItemModel, IngredientsModel, MenuItemIngredientsModel

router = APIRouter(
    prefix="/menu",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)
lib = MenuLib()


@router.get("/")
def get_menu():
    return lib.get_all_entries()

@router.get("/{name}")
def get_item_by_name(name):
    return lib.get_data_by_name(name)

@router.get("/{name}/ingredients")
def get_ingredients(name):
    return lib.get_ingredients_from_item(name)

@router.post("/add_new_item")
def add_new_item(request: MenuItemIngredientsModel):
    return lib.insert_new_item(request)