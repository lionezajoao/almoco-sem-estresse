from database.menu import MenuDatabase
from models.menu_models import MenuItemIngredientsModel

class MenuLib(MenuDatabase):
    def __init__(self):
        super().__init__()

    def get_all_entries(self):
        return self.get_menu()
    
    def get_data_by_name(self, name):
        return self.get_item_by_name(name)
    
    def get_ingredients_from_item(self, name):
        return self.get_item_ingredients(name)
    
    def insert_new_item(self, data: MenuItemIngredientsModel):
        if not self.check_if_item_exists(data.name):
            self.insert_item(data.name)

        for ingredient in data.ingredients:
            if not self.check_if_ingredient_exists(ingredient):
                self.insert_ingredient(ingredient)
            self.insert_item_ingredient(data.name, ingredient)