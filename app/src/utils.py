class Utils:
    def __init__(self) -> None:
        pass
    
    def transform_dataset(self,dataset):
        transformed_dataset = {}
        for dish, dish_type, ingredient, ingredient_category in dataset:
            if dish not in transformed_dataset:
                transformed_dataset[dish] = {
                    "type": dish_type,
                    "proteína": [],
                    "hortifruti": [],
                    "frio": [],
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