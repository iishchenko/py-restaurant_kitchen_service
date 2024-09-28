from app.models import DishType, Dish, Cook, Ingredient


def add_dish_type(new_dish_type):
    # Check if the dish type already exists in the database
    if DishType.objects.filter(name=new_dish_type).exists():
        return f"Dish type '{new_dish_type}' already exists."

    # Create and save the new dish type in the database
    DishType.objects.create(name=new_dish_type)
    return f"Dish type '{new_dish_type}' added successfully."


def create_cook(username, email, first_name, last_name, years_of_experience):
    # Check if a cook already exists with the same username or email
    if Cook.objects.filter(username=username).exists() or Cook.objects.filter(email=email).exists():
        return f"A cook with the username '{username}' or email '{email}' already exists."

    # Create and save the new cook in the database
    new_cook = Cook(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        years_of_experience=years_of_experience  # Correctly pass this value
    )
    new_cook.save()

    return f"A new cook has been created: {new_cook.username}"


def create_dish(dish_name, dish_type, cook_username, ingredients, price):
    try:
        # Get the dish type from the database using the ID (not name)
        dish_type = DishType.objects.get(id=dish_type)
    except DishType.DoesNotExist:
        return "Invalid dish type."

    # Check if the dish already exists in the given dish type
    if Dish.objects.filter(name=dish_name, dish_type=dish_type).exists():
        return f"{dish_name} already exists in {dish_type.name}."

    # Get or create the cook based on username
    try:
        cook = Cook.objects.get(username=cook_username)
    except Cook.DoesNotExist:
        return f"Cook with username '{cook_username}' does not exist."

    # Create a new dish
    new_dish = Dish.objects.create(
        name=dish_name,
        dish_type=dish_type,
        price=price
    )

    # Associate the cook with the dish
    new_dish.cooks.add(cook)

    # Add ingredients (assuming `ingredients` is a list)
    for ingredient_name in ingredients:
        ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name.strip())
        new_dish.ingredients.add(ingredient)

    new_dish.save()

    return f"{dish_name} has been added to {dish_type.name} by {cook_username}."


def update_dish(dish_name, new_dish_name=None, new_dish_type=None, new_cook_name=None, new_ingredients=None, price=None):
    try:
        # Check if dish_name is an ID (numeric) or a string (name)
        if str(dish_name).isdigit():
            dish = Dish.objects.get(id=dish_name)  # Query by ID if dish_name is numeric
        else:
            dish = Dish.objects.get(name=dish_name)  # Query by name if dish_name is a string
    except Dish.DoesNotExist:
        return f"Dish '{dish_name}' does not exist."

    # Update the dish name if provided
    if new_dish_name:
        dish.name = new_dish_name

    if new_dish_type:
        try:
            # Check if new_dish_type is an ID or a name
            if str(new_dish_type).isdigit():
                dish_type = DishType.objects.get(id=new_dish_type)  # Query by ID if it's numeric
            else:
                dish_type = DishType.objects.get(name=new_dish_type)  # Query by name if it's a string
            dish.dish_type = dish_type
        except DishType.DoesNotExist:
            return f"Invalid dish type '{new_dish_type}'."

    if new_cook_name:
        try:
            # Check if new_cook_name is an ID (numeric) or a username (string)
            if str(new_cook_name).isdigit():
                cook = Cook.objects.get(id=new_cook_name)  # Query by ID if it's numeric
            else:
                cook = Cook.objects.get(username=new_cook_name)  # Query by username if it's a string
            dish.cooks.set([cook])  # Replace current cooks with the new one
        except Cook.DoesNotExist:
            return f"Cook with identifier '{new_cook_name}' does not exist."

    # Update the ingredients if provided (assuming `new_ingredients` is a list)
    if new_ingredients:
        ingredient_objects = []
        for ingredient_name in new_ingredients:
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name.strip())
            ingredient_objects.append(ingredient)

        # Use .set() to replace the current ingredients with the new ones
        dish.ingredients.set(ingredient_objects)

    # Update the price if provided
    if price is not None:
        dish.price = price

    # Save the changes
    dish.save()

    return f"Dish '{dish.name}' has been updated successfully."


def delete_dish(dish_id):
    try:
        # Retrieve the dish by ID
        dish = Dish.objects.get(id=dish_id)

        # Store the dish type name for the message
        dish_type_name = dish.dish_type.name

        # Delete the dish
        dish.delete()

        # Return success message
        return f"Dish '{dish.name}' has been deleted from {dish_type_name}."

    except Dish.DoesNotExist:
        return f"Dish with ID '{dish_id}' does not exist."


def get_cook_for_dish(dish_id):
    try:
        # Get the dish by ID
        dish = Dish.objects.get(id=dish_id)

        # Get the cooks responsible for the dish (assuming a Many-to-Many relationship)
        cooks = dish.cooks.all()

        # If there are no cooks assigned
        if not cooks:
            return f"No cooks are currently assigned to the dish '{dish.name}'."

        # List all the cook usernames
        cook_names = ', '.join([cook.username for cook in cooks])
        return f"Cook(s) '{cook_names}' are responsible for the dish '{dish.name}'."

    except Dish.DoesNotExist:
        return f"Dish with ID '{dish_id}' does not exist."


def get_total_dish_types():
    # Count the number of distinct dish types in the database
    total_dish_types = DishType.objects.count()
    return total_dish_types


def get_total_dishes():
    # Count the total number of dishes in the database
    total_dishes = Dish.objects.count()
    return total_dishes


def count_cooks():
    # Use a set to store unique cook IDs or usernames
    unique_cooks = set()

    # Query all dishes and collect unique cooks
    dishes = Dish.objects.prefetch_related('cooks')  # Use prefetch_related for efficiency
    for dish in dishes:
        # Iterate over the cooks for each dish
        for cook in dish.cooks.all():
            unique_cooks.add(cook.username)  # Assuming you want to store cook usernames

    # Calculate the number of unique cooks
    number_of_cooks = len(unique_cooks)
    return number_of_cooks


def initialize_data():
    result = "\nMenu:\n"  # Start with a "Menu" heading

    # Loop through each dish type
    dish_types = DishType.objects.prefetch_related('dish_set')  # Prefetch dishes related to each dish type
    for dish_type in dish_types:
        # Append the category heading to the result
        result += f"\n--- {dish_type.name.capitalize()} ---\n"  # Assuming dish type has a 'name' field

        # Loop through each dish in the category
        dishes = dish_type.dish_set.all()  # Get all dishes related to this dish type
        for dish in dishes:
            # Append the dish details to the result
            result += f"Dish: {dish.name}\n"
            # Assuming there's a ManyToMany relationship with Cook
            cooks = ', '.join([cook.username for cook in dish.cooks.all()])  # Joining cook usernames
            result += f"Cooked by: {cooks}\n"
            result += f"Price: ${dish.price:.2f}\n"
            result += "Ingredients:\n"

            # Append each ingredient on a new line with proper indentation
            for ingredient in dish.ingredients.all():  # Assuming there's a ManyToMany relationship with Ingredient
                result += f"  - {ingredient.name}\n"  # Assuming ingredient has a 'name' field

            result += "\n"  # Add an extra newline after each dish

        # Append a separator between different categories
        result += "-" * 30 + "\n"

    return result  # Return the formatted string
