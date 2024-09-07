
dishes = {
    "main_course": {
        "Vareniki": {
            "ingredients": ["flour", "salt", "water"],
            "price": 8.99,
            "cook": "John"
        },
        "Tomato soup": {
            "ingredients": ["tomatoes", "chicken broth", "garlic", "onion", "butter", "flour", "sugar", "salt"],
            "price": 6.49,
            "cook": "John"
        },
        # Add more main_course dishes as needed
    },
    "dessert": {
        "Napoleon": {
            "ingredients": ["butter", "flour", "cream", "milk", "eggs", "sugar", "starch"],
            "price": 8.99,
            "cook": "Alice"
        },
        "Biscuits": {
            "ingredients": ["flour", "baking powder", "salt", "shortening", "milk"],
            "price": 3.29,
            "cook": "Alice"
        },
        # Add more dessert dishes as needed
    },
    "appetizer": {
        "Canapé": {
            "ingredients": ["salmon", "cream cheese", "bread", "tomato", "avocado", "cheese"],
            "price": 12.99,
            "cook": "Ira"
        },
        "Bruschetta": {
            "ingredients": ["bread", "tomato", "basil", "garlic", "olive oil", "salt"],
            "price": 7.99,
            "cook": "Ira"
        },
        "Stuffed Mushrooms": {
            "ingredients": ["mushrooms", "cheese", "breadcrumbs", "garlic", "parsley"],
            "price": 9.99,
            "cook": "Ira"
        }
        # Add more appetizer dishes as needed
    }
}


def add_dish_type(new_dish_type):
    if new_dish_type in dishes:
        return f"Dish type '{new_dish_type}' already exists."
    dishes[new_dish_type] = {}
    return f"Dish type '{new_dish_type}' added successfully."


def create_dish(dish_name, dish_type, cook_name, ingredients, price):
    if dish_type not in dishes:
        return "Invalid dish type."

    dish_dict = dishes[dish_type]

    if dish_name in dish_dict:
        return f"{dish_name} already exists in {dish_type}."

    new_dish = {"ingredients": ingredients, "price": price, "cook": cook_name}
    dish_dict[dish_name] = new_dish

    return f"{dish_name} has been added to {dish_type} by {cook_name}."


def update_dish(dish_name, new_dish_name=None, new_dish_type=None, new_cook_name=None, new_ingredients=None, price=None):
    current_dish_type = None
    dish_dict = None

    for dtype, dlist in dishes.items():
        if dish_name in dlist:
            current_dish_type = dtype
            dish_dict = dlist
            break

    if not dish_dict:
        return f"Dish '{dish_name}' does not exist."

    if new_dish_name:
        dish_dict[new_dish_name] = dish_dict.pop(dish_name)
        dish_name = new_dish_name

    if new_dish_type and new_dish_type != current_dish_type:
        dish_data = dish_dict.pop(dish_name)
        if new_dish_type in dishes:
            dishes[new_dish_type][dish_name] = dish_data
        else:
            return f"Invalid new dish type '{new_dish_type}'."

    if new_ingredients or price is not None:
        dish_data = dish_dict[dish_name]
        if new_ingredients:
            dish_data["ingredients"] = new_ingredients
        if price is not None:
            dish_data["price"] = price

    if new_cook_name:
        dish_dict[dish_name]["cook"] = new_cook_name

    return f"Dish '{dish_name}' has been updated successfully."


def delete_dish(dish_name):
    for dtype, dlist in dishes.items():
        if dish_name in dlist:
            del dlist[dish_name]
            return f"Dish '{dish_name}' has been deleted from {dtype}."

    return f"Dish '{dish_name}' does not exist."


def get_cook_for_dish(dish_name):
    for dish_type, dish_dict in dishes.items():
        if dish_name in dish_dict:
            cook_name = dish_dict[dish_name]["cook"]
            return f"Cook '{cook_name}' is responsible for the dish '{dish_name}'."
    return f"Dish '{dish_name}' does not exist."


def get_total_dish_types():
    total_dish_types = len(dishes)  # Number of keys in the main dictionary represents the dish types
    return total_dish_types


def get_total_dishes():
    # Calculate the number of dishes in each dish type
    dish_type_counts = {dish_type: len(dish_list) for dish_type, dish_list in dishes.items()}
    # Print the number of dishes in each dish type
    total_dishes = sum(dish_type_counts.values())
    return total_dishes


def count_cooks():
    # Initialize a set to store unique cooks
    unique_cooks = set()

    # Iterate over each dish type in the dishes dictionary
    for dish_type, dishes_in_type in dishes.items():
        # Iterate over each dish in the current dish type
        for dish_name, dish_details in dishes_in_type.items():
            cook = dish_details.get('cook')
            if cook:
                # Add the cook to the set of unique cooks
                unique_cooks.add(cook)

    # Calculate the number of unique cooks
    number_of_cooks = len(unique_cooks)
    return number_of_cooks


def initialize_data():
    result = ""  # Start with a "Menu" heading

    # Loop through each category of dishes
    for dish_type, dish_dict in dishes.items():
        # Append the category heading to the result
        result += f"\n--- {dish_type.capitalize()} ---\n"

        # Loop through each dish in the category
        for dish_name, dish_data in dish_dict.items():
            # Append the dish details to the result, ensuring each detail is on a new line
            result += f"Dish: {dish_name}\n"
            result += f"Cooked by: {dish_data['cook']}\n"
            result += f"Price: ${dish_data['price']:.2f}\n"
            result += "Ingredients:\n"

            # Append each ingredient on a new line with proper indentation
            for ingredient in dish_data["ingredients"]:
                result += f"  - {ingredient}\n"

            result += "\n"  # Add an extra newline after each dish

        # Append a separator between different categories
        result += "-" * 30 + "\n"

    return result  # Return the formatted string
