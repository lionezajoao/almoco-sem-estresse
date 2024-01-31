from fastapi import HTTPException
from fastapi.responses import JSONResponse 

from src.lib.menu import Menu
from models.menu_models import MenuItemIngredientsModel

class MenuController:
    def __init__(self):
        self.menu = Menu()

    def handle_all_items(self):
        return JSONResponse(content=self.menu.get_all_items(), status_code=200)
    
    def handle_data_by_type(self, type: str):
        return JSONResponse(content=self.menu.get_item_by_type(type), status_code=200)

    def handle_all_ingredients(self):
        return JSONResponse(content=self.menu.get_all_ingredients(), status_code=200)
    
    def handle_data_by_name(self, name):
        data = self.menu.get_item_by_name(name)
        if data:
            return JSONResponse(content=data, status_code=200)
        raise HTTPException(status_code=404, detail="Item not found")
    
    def handle_ingredients_by_name(self, name):
        data = self.menu.get_ingredients_by_name(name)
        if data:
            return JSONResponse(content=data, status_code=200)
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    def handle_ingredients_from_item(self, name):
        data = self.menu.get_ingredients_from_item(name)
        if data:
            return JSONResponse(content=data, status_code=200)
        raise HTTPException(status_code=404, detail="Item not found")
    
    def handle_insert_new_item(self, data: MenuItemIngredientsModel):
        try:
            item_check = self.menu.get_item_by_name(data.name)
            if item_check:
                raise HTTPException(status_code=400, detail="Item already exists")
            
            self.menu.insert_item(data.name)

            for ingredient in data.ingredients:
                if not self.menu.check_if_ingredient_exists(ingredient):
                    self.menu.insert_ingredient(ingredient)
                self.menu.insert_item_ingredient(data.name, ingredient)

            return JSONResponse(content={"message": "Item added successfully"}, status_code=200)
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")
