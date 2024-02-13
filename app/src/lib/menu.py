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

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for menu in data:
            pdf.cell(0, 10, f"Week Choice: {menu.week_choice}", ln=True)

            if isinstance(menu.data, list):
                for item in menu.data:
                    pdf.cell(0, 10, f"Weekday: {item.weekday}", ln=True)
                    pdf.cell(0, 10, f"Main Dish: {item.main_dish}", ln=True)
                    pdf.cell(0, 10, f"Salad: {item.salad}", ln=True)
                    pdf.cell(0, 10, f"Side Dish: {item.side_dish}", ln=True)
                    pdf.cell(0, 10, f"Accompaniment: {item.accompaniment}", ln=True)
            else:
                pdf.cell(0, 10, f"Weekday: {menu.data.weekday}", ln=True)
                pdf.cell(0, 10, f"Main Dish: {menu.data.main_dish}", ln=True)
                pdf.cell(0, 10, f"Salad: {menu.data.salad}", ln=True)
                pdf.cell(0, 10, f"Side Dish: {menu.data.side_dish}", ln=True)
                pdf.cell(0, 10, f"Accompaniment: {menu.data.accompaniment}", ln=True)

        pdf.output("menu.pdf")
