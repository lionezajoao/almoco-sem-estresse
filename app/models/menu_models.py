from pydantic import BaseModel
from typing import Optional, List

class MenuItemModel(BaseModel):
    name: str
    type: str

class IngredientsModel(BaseModel):
    name: str
    type: Optional[str] = None # Optional for existing ingredients. Required for new ingredients

class MenuItemIngredientsModel(BaseModel):
    name: str
    ingredients: List[IngredientsModel]
    type: Optional[str] = None # For detailed menu items, use this field. For simple menu items, leave this field blank.

class DataModel(BaseModel):
    weekday: str
    main_dish: Optional[str]
    salad: Optional[str]
    side_dish: Optional[str]
    accompaniment: Optional[str]
class MenuModel(BaseModel):
    week_choice: str
    data: List[DataModel]

class NewMenuModel(BaseModel):
    data: List[MenuModel]

