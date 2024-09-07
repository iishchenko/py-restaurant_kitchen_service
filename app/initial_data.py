from app.utils import dishes
from app.utils import add_dish_type, create_dish, update_dish, delete_dish, get_cook_for_dish


# Example usage of add_dish_type
print(add_dish_type("cocktail"))
print(dishes["cocktail"])

# Example usage of create_dish
print(create_dish("Lasagna", "main_course", "John", ["lasagna sheets", "ground beef", "tomato sauce", "cheese", "onion"], price=12.00))
print(create_dish("Brownies", "dessert", "Alice", ["butter", "sugar", "eggs", "cocoa powder", "flour", "baking powder"], price=13.00))
print(create_dish("Stuffed Peppers", "appetizer", "Ira", ["peppers", "rice", "ground beef", "cheese"], price=8.99))
print(create_dish("Caipirinha", "cocktail", "Bartender", ["cachaça", "sugar", "lime"], price=8.50))
print(create_dish("Espresso Martini", "cocktail", "Bartender", ["vodka", "espresso", "coffee liqueur"], price=10.00))
print(create_dish("Vareniki", "main_course", "John", ['flour', 'salt', 'water'], price=8.99))

# Example usage of update_dish
print(update_dish("Lasagna", new_dish_name="Vegetarian Lasagna", new_dish_type="main_course", new_cook_name="John", new_ingredients=["lasagna sheets", "spinach", "tomato sauce", "cheese", "onion"], price=12.00))

# Example usage of delete_dish
print(delete_dish("Vegetarian Lasagna"))
print(delete_dish("Brownies"))
print(delete_dish("Non-existent Dish"))

print(get_cook_for_dish("Vareniki"))
