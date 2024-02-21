from fpdf import FPDF
import pandas as pd

from src.utils import Utils
from src.lib.email_sender import EmailSender
from src.database.menu import MenuDatabase
from models.menu_models import NewMenuModel

class Menu(MenuDatabase):
    def __init__(self):
        super().__init__()
        self.utils = Utils()
        self.email = EmailSender()

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
    
    def get_all_items_ingredients(self):
        return self.get_relational_menu()
    
    def get_ingredient_type(self, ingredient):
        return self.get_ingredient_type_by_name(ingredient)
    
    def insert_new_item(self, data):
        if not self.check_if_item_exists(data.name):
            self.insert_item(data.name)

        for ingredient in data.ingredients:
            if not self.check_if_ingredient_exists(ingredient):
                self.insert_ingredient(ingredient)
            self.insert_item_ingredient(data.name, ingredient)

    def create_menu(self, data: NewMenuModel, token_data: dict):
        print("token_data", token_data)
        relational_data = self.utils.transform_dataset(self.get_all_items_ingredients())
        menu_data = {}
        ingredients_data = {}
        menu_name = f"Cardápio - { token_data.get('name') }"

        for item in data:
            menu_data[item.week_choice] = {}
            for day in item.data:
                main_dish_data = relational_data.get(day.main_dish)
                salad_data = relational_data.get(day.salad)
                side_dish_data = relational_data.get(day.side_dish)
                accompaniment_data = relational_data.get(day.accompaniment)

                menu_data[item.week_choice][day.weekday] = {
                    "main_dish": {
                        "dish": day.main_dish,
                        "ingredients": {
                            "protein": main_dish_data.get("proteína", []) if main_dish_data else [],
                            "hortifrutti": main_dish_data.get("hortifruti", []) if main_dish_data else [],
                            "cold_cuts": main_dish_data.get("frio", []) if main_dish_data else []
                        }
                    },
                    "salad": {
                        "dish": day.salad,
                        "ingredients": {
                            "protein": salad_data.get("proteína", []) if salad_data else [],
                            "hortifrutti": salad_data.get("hortifruti", []) if salad_data else [],
                            "cold_cuts": salad_data.get("frio", []) if salad_data else []
                        }
                    },
                    "side_dish": {
                        "dish": day.side_dish,
                        "ingredients": {
                            "protein": side_dish_data.get("proteína", []) if side_dish_data else [],
                            "hortifrutti": side_dish_data.get("hortifruti", []) if side_dish_data else [],
                            "cold_cuts": side_dish_data.get("frio", []) if side_dish_data else []
                        }
                    },
                    "accompaniment": {
                        "dish": day.accompaniment,
                        "ingredients": {
                            "protein": accompaniment_data.get("proteína", []) if accompaniment_data else [],
                            "hortifrutti": accompaniment_data.get("hortifruti", []) if accompaniment_data else [],
                            "cold_cuts": accompaniment_data.get("frio", []) if accompaniment_data else []
                        }
                    }
                }

        self.create_table(menu_data, menu_name)
        self.email.send_media_email(subject="Menu", recipients=[token_data.get("email")], attachment_path=f'temp/{ menu_name }.xlsx')

        return menu_data, ingredients_data
        

    def create_table(self, menu_data, menu_name):
        writer = pd.ExcelWriter(f'temp/{ menu_name }.xlsx', engine='xlsxwriter')
        monthly_ingredients = {'protein': set(), 'hortifrutti': set(), 'cold_cuts': set()}

        for week_choice, week_data in menu_data.items():
            table_data = []

            for weekday, day_data in week_data.items():
                main_dish = day_data["main_dish"]["dish"]
                salad = day_data["salad"]["dish"]
                side_dish = day_data["side_dish"]["dish"]
                accompaniment = day_data["accompaniment"]["dish"]

                main_dish_ingredients = ", ".join(day_data["main_dish"]["ingredients"]["protein"] + day_data["main_dish"]["ingredients"]["hortifrutti"] + day_data["main_dish"]["ingredients"].get("cold_cuts", []))
                salad_ingredients = ", ".join(day_data["salad"]["ingredients"]["protein"] + day_data["salad"]["ingredients"]["hortifrutti"] + day_data["salad"]["ingredients"].get("cold_cuts", []))
                side_dish_ingredients = ", ".join(day_data["side_dish"]["ingredients"]["protein"] + day_data["side_dish"]["ingredients"]["hortifrutti"] + day_data["side_dish"]["ingredients"].get("cold_cuts", []))
                accompaniment_ingredients = ", ".join(day_data["accompaniment"]["ingredients"]["protein"] + day_data["accompaniment"]["ingredients"]["hortifrutti"] + day_data["accompaniment"]["ingredients"].get("cold_cuts", []))

                table_data.append([self.utils.handle_week_day(weekday), main_dish, salad, side_dish, accompaniment, main_dish_ingredients, salad_ingredients, side_dish_ingredients, accompaniment_ingredients])

                for ingredient_type in ['protein', 'hortifrutti', 'cold_cuts']:
                    monthly_ingredients[ingredient_type].update(day_data["main_dish"]["ingredients"].get(ingredient_type, []) + day_data["salad"]["ingredients"].get(ingredient_type, []) + day_data["side_dish"]["ingredients"].get(ingredient_type, []) + day_data["accompaniment"]["ingredients"].get(ingredient_type, []))

            columns = ["Dia da Semana", "Prato Principal", "Salada", "Acompanhamento", "Guarnição", "Ingredientes Prato Principal", "Ingredientes Salada", "Ingredientes Acompanhamento", "Ingredientes Guarnição"]
            df = pd.DataFrame(table_data, columns=columns)
            df.to_excel(writer, sheet_name=f"Semana {week_choice}", index=False)

        max_length = max(len(monthly_ingredients["protein"]), len(monthly_ingredients["hortifrutti"]), len(monthly_ingredients["cold_cuts"]))

        # Extend the shorter lists with None to match the max_length
        proteins = list(monthly_ingredients["protein"]) + [None] * (max_length - len(monthly_ingredients["protein"]))
        hortifruti = list(monthly_ingredients["hortifrutti"]) + [None] * (max_length - len(monthly_ingredients["hortifrutti"]))
        cold_cuts = list(monthly_ingredients["cold_cuts"]) + [None] * (max_length - len(monthly_ingredients["cold_cuts"]))

        monthly_ingredients_df = pd.DataFrame({
            "Proteína": proteins,
            "Hortifruti": hortifruti,
            "Frios": cold_cuts
        })

        monthly_ingredients_df.to_excel(writer, sheet_name="Ingredientes do Mês", index=False)


        writer.close()

