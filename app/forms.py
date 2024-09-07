from django import forms
from app.utils import dishes


class DishTypeForm(forms.Form):
    dish_type = forms.CharField(label='Dish Type', max_length=100)


class CreateDishForm(forms.Form):
    dish_name = forms.CharField(label='Dish Name', max_length=100)
    dish_type = forms.ChoiceField(label='Dish Type')
    cook_name = forms.CharField(label='Cook Name', max_length=100)
    ingredients = forms.CharField(
        label='Ingredients',
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text='Enter ingredients separated by commas.'
    )
    price = forms.DecimalField(label='Price', max_digits=5, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super(CreateDishForm, self).__init__(*args, **kwargs)

        # Dynamically generate the choices based on the current state of dishes
        self.fields['dish_type'].choices = [(key, key.replace('_', ' ').capitalize()) for key in dishes.keys()]


class UpdateDishForm(forms.Form):
    # Dynamically generate dish name choices from the dishes dictionary
    dish_name = forms.ChoiceField(
        label='Current Dish Name',
        choices=[]  # Initialize with an empty list, will be populated in __init__
    )
    new_dish_name = forms.CharField(label='New Dish Name', max_length=100, required=False)
    new_dish_type = forms.ChoiceField(
        label='New Dish Type',
        choices=[],  # Will be populated in __init__
    )
    new_cook_name = forms.CharField(label='New Cook Name', max_length=100, required=False)
    new_ingredients = forms.CharField(
        label='New Ingredients',
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text='Enter ingredients separated by commas.',
        required=False
    )
    price = forms.DecimalField(label='New Price', max_digits=5, decimal_places=2, required=False)

    def __init__(self, *args, **kwargs):
        super(UpdateDishForm, self).__init__(*args, **kwargs)

        # Populate dish_name choices dynamically
        self.fields['dish_name'].choices = [(name, name) for dtype, dishes_list in dishes.items() for name in dishes_list.keys()]

        # Initialize dish_type choices as empty; they will be filled by JavaScript
        self.fields['new_dish_type'].choices = [(key, key.replace('_', ' ').capitalize()) for key in dishes.keys()]

        # Store the entire dishes dictionary in a hidden field (optional)
        # to use in JavaScript if needed for more advanced dynamic behavior.
        self.dishes_data = dishes  # You can pass this to the template if needed


class DeleteDishForm(forms.Form):
    # Dynamically generate dish name choices from the dishes dictionary
    dish_name = forms.ChoiceField(
        label='Dish Name',
        choices=[],  # Initialize with an empty list, will be populated in __init__
    )

    def __init__(self, *args, **kwargs):
        super(DeleteDishForm, self).__init__(*args, **kwargs)

        # Populate dish_name choices dynamically
        self.fields['dish_name'].choices = [(name, name) for dtype, dishes_list in dishes.items() for name in dishes_list.keys()]


class GetCookForDishForm(forms.Form):
    dish_name = forms.ChoiceField(
        label='Dish Name',
        choices=[],  # Choices will be populated dynamically
    )

    def __init__(self, *args, **kwargs):
        super(GetCookForDishForm, self).__init__(*args, **kwargs)
        # Populate dish_name choices dynamically
        self.fields['dish_name'].choices = [(name, name) for dtype, dishes_list in dishes.items() for name in dishes_list.keys()]