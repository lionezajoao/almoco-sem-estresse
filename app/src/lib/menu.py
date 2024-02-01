from fpdf import FPDF

from src.database.menu import MenuDatabase
class Menu(MenuDatabase):
    def __init__(self):
        super().__init__()

    def get_all_items(self):
        data = self.get_menu()
        return data
    
    def get_item_by_type(self, type):
        data = self.get_data_by_type(type)
        return [item[0] for item in data]
    
    def get_all_ingredients(self):
        return self.get_ingredients()
    
    def get_data_by_name(self, name):
        return self.get_item_by_name(name)
    
    def get_ingredients_from_items(self, name):
        return self.get_items_ingredients(name)
    
    def insert_new_item(self, data):
        if not self.check_if_item_exists(data.name):
            self.insert_item(data.name)

        for ingredient in data.ingredients:
            if not self.check_if_ingredient_exists(ingredient):
                self.insert_ingredient(ingredient)
            self.insert_item_ingredient(data.name, ingredient)

    def create_menu(self, data):
        weekday = data.weekday
        main_dish = data.main_dish
        salad = data.salad
        side_dish = data.side_dish
        accompaniment = data.accompaniment

        ingredient_list = self.get_ingredients_from_items([main_dish, salad, side_dish, accompaniment])
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        for ingredient in ingredient_list:
            pdf.cell(0, 10, ingredient, ln=True)
        
        pdf.output("ingredients.pdf")