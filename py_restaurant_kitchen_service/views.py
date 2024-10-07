from django.contrib.auth import authenticate
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from app.forms import DishTypeForm, CreateDishForm, UpdateDishForm, DeleteDishForm, GetCookForDishForm, SignUpForm
from django.views.generic import TemplateView
from django.template import TemplateDoesNotExist
from app.forms import CreateCookForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from app.models import DishType, Dish, Cook, Ingredient


class RegisterUserView(View):
    template_name = "accounts/register.html"

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        msg = None
        success = False

        if form.is_valid():
            user = form.save()  # Save the user instance
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")

            # Authenticate the user after registration
            user = authenticate(username=username, password=raw_password)

            if user is not None:
                msg = 'User created - please <a href="/login">login</a>.'
                success = True
                return redirect("/login/")
            else:
                msg = 'Authentication failed. Please try again.'
        else:
            msg = 'Form is not valid: ' + str(form.errors)

        return render(request, self.template_name, {"form": form, "msg": msg, "success": success})


class SignUpView(TemplateView):
    template_name = "catalog/page-sign-up.html"


class SignInView(TemplateView):
    template_name = "catalog/page-sign-in.html"


class LogoutView(View):
    template_name = 'accounts/logout.html'  # Adjust the path as needed

    def get(self, request, *args, **kwargs):
        # Log out the user when accessing the logout page via GET request
        logout(request)
        # Redirect to the login page or any other page after logout
        return redirect('login')  # Replace 'login' with your desired URL

    def post(self, request, *args, **kwargs):
        # Log out the user when the logout form is submitted
        logout(request)
        return redirect('login')  # Or render a logout confirmation page if needed


class AddDishTypeView(FormView):
    template_name = 'catalog/dish_type.html'
    form_class = DishTypeForm
    success_url = reverse_lazy('catalog:dish_type_list')  # Redirect after successful addition

    def form_valid(self, form):
        # Get the new dish type from the form
        new_dish_type = form.cleaned_data['dish_type']

        # Call the add_dish_type method and get the message
        message = self.add_dish_type(new_dish_type)

        # Pass the message to the context
        context = self.get_context_data(form=form, message=message)

        # Render the form with the message
        return self.render_to_response(context)

    def add_dish_type(self, new_dish_type):
        # Check if the dish type already exists in the database
        if DishType.objects.filter(name=new_dish_type).exists():
            return f"Dish type '{new_dish_type}' already exists."

        # Create and save the new dish type in the database
        DishType.objects.create(name=new_dish_type)
        return f"Dish type '{new_dish_type}' added successfully."

    def form_invalid(self, form):
        # Handle the case where the form is invalid
        return self.render_to_response(self.get_context_data(form=form, message="Please correct the errors below."))


class CreateCookView(FormView):
    template_name = 'catalog/create_cook.html'
    form_class = CreateCookForm
    success_url = reverse_lazy('catalog:cook_list')  # Redirect after successful creation

    def form_valid(self, form):
        # Get form data
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        years_of_experience = form.cleaned_data['years_of_experience']

        # Call the create_cook method and get the message
        message = self.create_cook(username, email, first_name, last_name, years_of_experience)

        # Pass the message to the context
        context = self.get_context_data(form=form, message=message)

        # Render the form with the message
        return self.render_to_response(context)

    def create_cook(self, username, email, first_name, last_name, years_of_experience):
        # Check if a cook already exists with the same username or email
        if Cook.objects.filter(username=username).exists() or Cook.objects.filter(email=email).exists():
            return f"A cook with the username '{username}' or email '{email}' already exists."

        # Create and save the new cook in the database
        new_cook = Cook(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            years_of_experience=years_of_experience
        )
        new_cook.save()

        return f"A new cook has been created: {new_cook.username}"

    def form_invalid(self, form):
        # Handle the case where the form is invalid
        return self.render_to_response(self.get_context_data(form=form, message="A cook with the username '{username}' or email '{email}' already exists."))


class CreateDishView(FormView):
    template_name = 'catalog/create_dish.html'
    form_class = CreateDishForm
    success_url = reverse_lazy('catalog:dish_list')  # Redirect after successful creation

    def form_valid(self, form):
        # Get form data
        dish_name = form.cleaned_data['dish_name']
        dish_type = form.cleaned_data['dish_type']
        cook_username = form.cleaned_data['cook_name']
        ingredients = form.cleaned_data['ingredients'].split(',')  # Convert input string to list
        price = form.cleaned_data['price']

        # Call the create_dish method and get the message
        message = self.create_dish(dish_name, dish_type, cook_username, ingredients, price)

        # Pass the message to the context
        context = self.get_context_data(form=form, message=message)

        # Reset the form after submission
        context['form'] = self.form_class()

        # Render the form with the message
        return self.render_to_response(context)

    def create_dish(self, dish_name, dish_type, cook_username, ingredients, price):
        # Get the dish type from the database using the ID (not name)
        try:
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

    def form_invalid(self, form):
        # Handle the case where the form is invalid
        return self.render_to_response(self.get_context_data(form=form, message="Please correct the errors below."))


class UpdateDishView(FormView):
    template_name = 'catalog/update_dish.html'
    form_class = UpdateDishForm
    success_url = reverse_lazy('catalog:dish_list')  # Redirect after successful update

    def form_valid(self, form):
        # Extract form data
        dish_id = form.cleaned_data['dish_name']
        new_dish_name = form.cleaned_data.get('new_dish_name')
        new_dish_type = form.cleaned_data.get('new_dish_type')
        new_cook_name = form.cleaned_data.get('new_cook_name')
        new_ingredients = form.cleaned_data.get('new_ingredients')
        price = form.cleaned_data.get('price')

        # Call the update_dish method and get the result message
        message = self.update_dish(
            dish_name=dish_id,
            new_dish_name=new_dish_name,
            new_dish_type=new_dish_type,
            new_cook_name=new_cook_name,
            new_ingredients=new_ingredients.split(',') if new_ingredients else None,  # Split ingredients if provided
            price=price
        )

        # Pass the message to the context
        context = self.get_context_data(form=form, message=message)

        # Render the form with the message
        return self.render_to_response(context)

    def update_dish(self, dish_name, new_dish_name=None, new_dish_type=None, new_cook_name=None, new_ingredients=None, price=None):
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

    def form_invalid(self, form):
        # Handle the case where the form is invalid
        return self.render_to_response(self.get_context_data(form=form, message="Please correct the errors below."))


class DeleteDishView(FormView):
    template_name = 'catalog/delete_dish.html'
    form_class = DeleteDishForm
    success_url = reverse_lazy('catalog:dish_list')  # Redirect after successful deletion

    def form_valid(self, form):
        # Get the dish ID from the form
        dish_id = form.cleaned_data['dish_name']

        # Call the delete_dish method and get the message
        message = self.delete_dish(dish_id)

        # Pass the message to the context
        context = self.get_context_data(form=form, message=message)

        # Render the form with the message
        return self.render_to_response(context)

    def delete_dish(self, dish_id):
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
            # Return an error message with dish_name instead of dish_id
            return f"Dish with name '{dish_id}' does not exist."


class GetCookForDishView(FormView):
    template_name = 'catalog/get_cook_for_dish.html'
    form_class = GetCookForDishForm
    success_url = ''  # You can set a URL to redirect after the form is processed if needed

    def form_valid(self, form):
        # Get the selected dish ID from the form
        dish_id = form.cleaned_data['dish_name']

        # Call get_cook_for_dish method with the dish ID
        message = self.get_cook_for_dish(dish_id)

        # Pass the message to the context
        context = self.get_context_data(form=form, message=message)

        # Render the form with the message
        return self.render_to_response(context)

    def get_cook_for_dish(self, dish_id):
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

    def form_invalid(self, form):
        # Handle the case where the form is invalid
        return self.render_to_response(self.get_context_data(form=form, message="Please correct the errors below."))


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = 'login/'
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Initialize context data
        context['segment'] = 'index'
        context['menu'] = self.initialize_data()
        context['number_of_cooks'] = self.count_cooks()
        context['total_dish_types'] = self.get_total_dish_types()
        context['total_dishes'] = self.get_total_dishes()

        return context

    def get_total_dish_types(self):
        # Count the number of distinct dish types in the database
        total_dish_types = DishType.objects.count()
        return total_dish_types

    def get_total_dishes(self):
        # Count the total number of dishes in the database
        total_dishes = Dish.objects.count()
        return total_dishes

    def count_cooks(self):
        # Use a set to store unique cook usernames
        unique_cooks = set()

        # Query all dishes and collect unique cooks
        dishes = Dish.objects.prefetch_related('cooks')  # Use prefetch_related for efficiency
        for dish in dishes:
            # Iterate over the cooks for each dish
            for cook in dish.cooks.all():
                unique_cooks.add(cook.username)  # Store cook usernames

        # Calculate the number of unique cooks
        number_of_cooks = len(unique_cooks)
        return number_of_cooks

    def initialize_data(self):
        result = "\nMenu:\n"  # Start with a "Menu" heading

        # Loop through each dish type
        dish_types = DishType.objects.prefetch_related('dish_set')  # Prefetch dishes related to each dish type
        for dish_type in dish_types:
            # Append the category heading to the result
            result += f"\n--- {dish_type.name.capitalize()} ---\n"

            # Loop through each dish in the category
            dishes = dish_type.dish_set.all()  # Get all dishes related to this dish type
            for dish in dishes:
                # Append the dish details to the result
                result += f"Dish: {dish.name}\n"
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


class PagesView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        context = {}

        try:
            # Extract the template name from the request path
            load_template = request.path.split('/')[-1]

            # Redirect if the template is 'admin'
            if load_template == 'admin':
                return HttpResponseRedirect(reverse('admin:index'))

            context['segment'] = load_template

            # Load the appropriate template
            html_template = loader.get_template(f'catalog/{load_template}')
            return HttpResponse(html_template.render(context, request))

        except TemplateDoesNotExist:
            # Handle 404 error if the template does not exist
            html_template = loader.get_template('catalog/page-404.html')
            return HttpResponse(html_template.render(context, request))

        except Exception:
            # Handle any other error with a 500 page
            html_template = loader.get_template('catalog/page-500.html')
            return HttpResponse(html_template.render(context, request))
