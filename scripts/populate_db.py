import pandas as pd
from tqdm import tqdm

from app.src.database.menu import MenuDatabase
from app.models.menu_models import IngredientsModel, MenuItemIngredientsModel


def create_tables(db):
    db.logger.info("Creating tables...")

    db.create("""CREATE TABLE IF NOT EXISTS "users" (
        "_id" uuid PRIMARY KEY,
        "name" varchar NOT NULL,
        "email" varchar NOT NULL,
        "password" varchar NOT NULL,
        "role" varchar NOT NULL
        );""")
    
    db.create("""CREATE TABLE IF NOT EXISTS "items" (
        "_id" uuid PRIMARY KEY,
        "name" varchar NOT NULL UNIQUE,
        "type" varchar NOT NULL
        );""")
    
    db.create("""CREATE TABLE IF NOT EXISTS "ingredients" (
        "_id" uuid PRIMARY KEY,
        "name" varchar NOT NULL UNIQUE,
        "type" varchar NOT NULL
        );""")
    
    db.create("""CREATE TABLE IF NOT EXISTS "item_ingredients" (
        "item_id" uuid NOT NULL,
        "ingredient_id" uuid NOT NULL,
        FOREIGN KEY (item_id) REFERENCES items(_id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredients(_id)
        );""")

def insert_data(db, data):
    db.logger.info("Populating database...")
    for item in tqdm(data):
        db.insert_item(item.name, item.type)
        for ingredient in item.ingredients:
            db.insert_ingredient(ingredient.name, ingredient.type)
            db.insert_item_ingredient(item.name, ingredient.name)

    db.logger.info("Normalizing database...")
    db.update("UPDATE ingredients SET name = TRIM(TRAILING FROM name);")
    db.update("UPDATE items SET name = TRIM(TRAILING FROM name);")
    db.logger.info("Database populated successfully!")

def handle_dataset(df, sheet_name):

    data = {}
    for _, row in df.iterrows():
        protein = row.get('Proteína')
        mercearia_components = [row[col] for col in df.columns if 'Mercearia Componente' in col]
        hortifruti_components = [row[col] for col in df.columns if 'Hortifruti Componente' in col]
        frios_components = [row[col] for col in df.columns if 'Frios Componente' in col]

        data[row[sheet_name]] = {
            'protein': protein,
            'mercearia_components': mercearia_components,
            'hortifruti_components': hortifruti_components,
            'frios_components': frios_components,
            'type': sheet_name if sheet_name != 'Guarnição' else 'Acompanhamentos'
        }
        
    return data

if __name__ == "__main__":

    db = MenuDatabase()
    full_data = {}
    menu_items = []
    sheet_names = ['Prato Principal Input', 'Acompanhamentos Input', 'Saladas Input', 'Guarnição Input']

    db.connect()

    try:
        create_tables(db)
    except Exception as e:
        db.logger.error(f"Error creating tables, reason: {e}")
        db.close()

    for sheet in sheet_names:
        df = pd.read_excel('./temp/base.xlsx', sheet_name=sheet)
        full_data.update(handle_dataset(df, sheet.removesuffix(' Input')))

    db.logger.info("Populating database...")
    
    for key, value in full_data.items():

        if pd.notna(key):
            ingredients = []
            if pd.notna(value["protein"]):
                ingredient = IngredientsModel(name=value["protein"], type="Proteina")
                ingredients.append(ingredient)
            for component in value["mercearia_components"]:
                if pd.notna(component):
                    ingredient = IngredientsModel(name=component, type="Mercearia")
                    ingredients.append(ingredient)
            for component in value["hortifruti_components"]:
                if pd.notna(component):
                    ingredient = IngredientsModel(name=component, type="Hortifruti")
                    ingredients.append(ingredient)
            for component in value["frios_components"]:
                if pd.notna(component):
                    ingredient = IngredientsModel(name=component, type="Frios")
                    ingredients.append(ingredient)

            menu_item = MenuItemIngredientsModel(name=key, ingredients=ingredients, type=value["type"])
            menu_items.append(menu_item)

    try:
        insert_data(db, menu_items)
    except Exception as e:
        db.logger.error(f"Error inserting data, reason: {e}")
        db.close()    

    db.close()
    
