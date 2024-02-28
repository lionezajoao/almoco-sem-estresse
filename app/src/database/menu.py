import uuid
from app.src.database.base import Database

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

    def get_items_ingredients(self, name: str) -> list:
        query = """
        SELECT name FROM ingredients
        WHERE _id IN (
            SELECT item_id FROM item_ingredients
            WHERE menu_id IN (
                SELECT _id FROM items WHERE name = %s
            )
        );"""
        
        params = (name,)
        result = self.query(query, params)
        return [row[0] for row in result]
    
    def get_ingredient_type_by_name(self, name: str) -> str:
        query = "SELECT type FROM ingredients WHERE name = %s"
        params = (name,)
        result = self.query(query, params)
        if result:
            return result[0][0]
        
    def get_relational_menu(self):
        query = """
        SELECT items.name AS item_name,
            items.type AS item_type,
            ing.name   AS ingredient_name,
            ing.type   AS ingredient_type
        FROM items
                LEFT JOIN item_ingredients ii ON items._id = ii.menu_id
                LEFT JOIN ingredients ing ON ii.item_id = ing._id
        WHERE ing.name IS NOT NULL
        AND ing.type IS NOT NULL;"""
        return self.query(query)
    
    def insert_item(self, name: str, ingredient_type: str):
        query = "INSERT INTO items (_id, name, type) VALUES (%s, %s, %s)"
        params = (str(uuid.uuid4()), name, ingredient_type,)
        self.insert(query, params)

    def insert_ingredient(self, name: str, ingredient_type: str):
        query = "INSERT INTO ingredients (_id, name, type) VALUES (%s, %s, %s)"
        params = (str(uuid.uuid4()), name, ingredient_type,)
        self.insert(query, params)

    def insert_item_ingredient(self, item_name: str, ingredient_name: str):
        query = """
        INSERT INTO item_ingredients (menu_id, item_id)
        VALUES (
            (SELECT _id FROM items WHERE name = %s),
            (SELECT _id FROM ingredients WHERE name = %s)
        );"""
        params = (item_name, ingredient_name)
        self.insert(query, params)