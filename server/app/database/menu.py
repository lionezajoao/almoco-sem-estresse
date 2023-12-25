from database.base import Database

class MenuDatabase(Database):
    def __init__(self):
        super().__init__()

    def get_menu(self):
        query = "SELECT * FROM main_menu;"
        return self.query(query)
    
    def get_item_by_name(self, name: str) -> list:
        query = "SELECT * FROM main_menu WHERE name = %s"
        params = (name,)
        return self.query(query, params)
    
    def get_ingredients_by_name(self, name: str) -> list:
        query = "SELECT * FROM items WHERE name = %s"
        params = (name,)
        return self.query(query, params)
    
    def check_if_item_exists(self, name: str) -> bool:
        return False
        try:
            self.get_item_by_name(name)
            return True
        except:
            return False
    
    def check_if_ingredient_exists(self, name: str) -> bool:
        try:
            self.get_ingredients_by_name(name)
            return True
        except:
            return False

    def get_item_ingredients(self, name: str) -> list:
        query = """
        select name from items
        where _id in (
            select item_id from menu_items
            where menu_id = (
                select _id
                from main_menu where name = %s));"""
        
        params = (name,)
        result = self.query(query, params)
        return [row[0] for row in result]
    
    def insert_item(self, name: str):
        query = "INSERT INTO main_menu (name) VALUES (%s)"
        params = (name,)
        self.insert(query, params)

    def insert_ingredient(self, name: str):
        query = "INSERT INTO items (name) VALUES (%s)"
        params = (name,)
        self.insert(query, params)

    def insert_item_ingredient(self, item_name: str, ingredient_name: str):
        query = """
        INSERT INTO menu_items (menu_id, item_id)
        VALUES (
            (SELECT _id FROM main_menu WHERE name = %s),
            (SELECT _id FROM items WHERE name = %s)
        );"""
        params = (item_name, ingredient_name)
        self.insert(query, params)