import random
import string
import logging
from logging.config import fileConfig

class Utils:
    def __init__(self) -> None:
        fileConfig('logging_config.ini')
        self.logger = logging.getLogger()

    @staticmethod
    def log(func):
        def wrapper(*args, **kwargs):
            try:
                # Log the start of the function
                Utils().logger.debug(f"Calling function {func.__name__}")
                
                # Call the original function
                result = func(*args, **kwargs)
                
                # Log the end of the function
                Utils().logger.debug(f"Function {func.__name__} completed")
                
                return result
            except Exception as e:
                # Log the error
                Utils().logger.error(f"Error in function {func.__name__}: {str(e)}")
                raise
        return wrapper
    
    def transform_dataset(self, dataset):
        transformed_dataset = {}
        for dish, dish_type, ingredient, ingredient_category in dataset:
            if dish not in transformed_dataset:
                transformed_dataset[dish] = {
                    "type": dish_type,
                    "proteina": [],
                    "hortifruti": [],
                    "frios": [],
                    "mercearia": []
                    # Add other categories as needed based on your dataset
                }

            if ingredient and ingredient_category:
                category_key = ingredient_category.lower()  # Normalize the category key
                if category_key in transformed_dataset[dish]:
                    transformed_dataset[dish][category_key].append(ingredient)
                else:
                    # If a new category is found, add it dynamically
                    transformed_dataset[dish][category_key] = [ingredient]

        return transformed_dataset
    
    def generate_random_password(self, length):
        
        characters = string.ascii_letters + string.digits + "!@#$&"
        password = ""
        for _ in range(length):
            random_index = random.randint(0, len(characters) - 1)
            password += characters[random_index]
        return password
    
    def handle_week_day(self, week_day):
        switcher = {
            "mon": "Segunda-feira",
            "tue": "Terça-feira",
            "wed": "Quarta-feira",
            "thu": "Quinta-feira",
            "fri": "Sexta-feira",
            "Segunda-feira": "mon",
            "Terça-feira": "tue",
            "Quarta-feira": "wed",
            "Quinta-feira": "thu",
            "Sexta-feira": "fri"
        }
        return switcher.get(week_day, "Invalid day")