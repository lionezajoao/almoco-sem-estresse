from src.database.base import Database

class MenuDatabase(Database):
    def __init__(self):
        super().__init__()

    def get_menu(self):
        query = "SELECT name, type FROM items;"
        return self.query(query)
    
    def get_ingredients(self):
        query = "SELECT name, type FROM ingredients;"
        return self.query(query)
    
    def get_data_by_type(self, type: str) -> list:
        query = "SELECT name FROM items WHERE type = %s"
        params = (type,)
        return self.query(query, params)
    
    def get_item_by_name(self, name: str) -> list:
        query = "SELECT name, type FROM items WHERE name = %s"
        params = (name,)
        result = self.query(query, params)
        if result:
            return dict(zip(('name', 'type'), result[0]))
        return result
    
    def get_ingredients_by_name(self, name: str) -> list:
        query = "SELECT name, type FROM ingredients WHERE name = %s"
        params = (name,)
        data = self.query(query, params)
        if data:
            return dict(zip(('name', 'type'), data[0]))
        return data
    
    def check_if_item_exists(self, name: str) -> bool:
        if self.get_item_by_name(name):
            return True
    
    def check_if_ingredient_exists(self, name: str) -> bool:
        if self.get_ingredients_by_name(name):
            return True

    def get_item_ingredients(self, name: str) -> list:
        query = """
        select name from ingredients
        where _id in (
            select item_id from item_ingredients
            where menu_id = (
                select _id
                from items where name = %s));"""
        
        params = (name,)
        result = self.query(query, params)
        return [row[0] for row in result]
    
    def insert_item(self, name: str):
        query = "INSERT INTO items (name) VALUES (%s)"
        params = (name,)
        self.insert(query, params)

    def insert_ingredient(self, name: str):
        query = "INSERT INTO ingredients (name) VALUES (%s)"
        params = (name,)
        self.insert(query, params)

    def insert_item_ingredient(self, item_name: str, ingredient_name: str):
        query = """
        INSERT INTO menu_items (menu_id, item_id)
        VALUES (
            (SELECT _id FROM items WHERE name = %s),
            (SELECT _id FROM ingredients WHERE name = %s)
        );"""
        params = (item_name, ingredient_name)
        self.insert(query, params)