from fastapi import HTTPException
from fastapi.responses import JSONResponse 

from app.src.lib.menu import Menu
from app.src.lib.user import User
from app.models.menu_models import MenuItemIngredientsModel

class MenuController:
    def __init__(self):
        self.menu = Menu()
        self.user = User()
        self.scope = ["admin"]

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
    
    def handle_insert_new_item(self, data: MenuItemIngredientsModel, token_data: dict):
        if not self.user.verify_user_role(token_data.get("email"), token_data.get("role"), self.scope):
            raise HTTPException(status_code=401, detail="Unauthorized")
        try:
            item_check = self.menu.get_item_by_name(data.name)
            if item_check:
                raise HTTPException(status_code=400, detail="Item already exists")
            
            self.menu.insert_item(data.name, data.type)

            for ingredient in data.ingredients:
                if not self.menu.check_if_ingredient_exists(ingredient.name):
                    self.menu.insert_ingredient(ingredient.name, ingredient.type)
                self.menu.insert_item_ingredient(data.name, ingredient.name)

            return JSONResponse(content={"success": True, "message": "Item added successfully"}, status_code=200)
        
        except Exception as e:
            print(e)
            self.menu.rollback()
            raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")
        
    def handle_create_menu(self, request, token_data):
        try:
            return JSONResponse(content=self.menu.create_menu(request.data, token_data), status_code=200)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")
