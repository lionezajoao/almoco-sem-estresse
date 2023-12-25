from pydantic import BaseModel
from typing import Optional, List

class MenuItemModel(BaseModel):
    name: str
    type: str

class IngredientsModel(BaseModel):
    name: str
    type: str

class MenuItemIngredientsModel(BaseModel):
    name: str
    ingredients: List[str or IngredientsModel] # For new ingredients, use the IngredientsModel. For existing ingredients, use the string.
    type: Optional[str] = None # For detailed menu items, use this field. For simple menu items, leave this field blank.
