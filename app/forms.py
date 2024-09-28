from django import forms
from app.models import DishType, Cook, Dish


class DishTypeForm(forms.Form):
    dish_type = forms.CharField(label='Dish Type', max_length=100)


class CreateCookForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = ['username', 'email', 'first_name', 'last_name', 'years_of_experience']  # Specify the fields you want in the form


class CreateDishForm(forms.Form):
    dish_name = forms.CharField(label='Dish Name', max_length=100)
    dish_type = forms.ChoiceField(label='Dish Type')
    cook_name = forms.ChoiceField(label='Cook Name')  # Will display cook usernames
    ingredients = forms.CharField(
        label='Ingredients',
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text='Enter ingredients separated by commas.'
    )
    price = forms.DecimalField(label='Price', max_digits=5, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super(CreateDishForm, self).__init__(*args, **kwargs)

        # Dynamically generate the choices for dish_type based on the current state of the DishType model
        self.fields['dish_type'].choices = [
            (dish_type.id, dish_type.name) for dish_type in DishType.objects.all()
        ]

        # Dynamically generate the choices for cook_name based on the current state of the Cook model
        self.fields['cook_name'].choices = [
            (cook.username, f"{cook.first_name} {cook.last_name}") for cook in Cook.objects.all()
        ]


class UpdateDishForm(forms.Form):
    # Dynamically generate dish name choices from the Dish model
    dish_name = forms.ChoiceField(
        label='Current Dish Name',
        choices=[],  # Will be populated in __init__
    )
    new_dish_name = forms.CharField(label='New Dish Name', max_length=100, required=False)
    new_dish_type = forms.ChoiceField(
        label='New Dish Type',
        choices=[],  # Will be populated in __init__
    )
    new_cook_name = forms.ChoiceField(label='New Cook Name', choices=[], required=False)
    new_ingredients = forms.CharField(
        label='New Ingredients',
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text='Enter ingredients separated by commas.',
        required=False
    )
    price = forms.DecimalField(label='New Price', max_digits=5, decimal_places=2, required=False)

    def __init__(self, *args, **kwargs):
        super(UpdateDishForm, self).__init__(*args, **kwargs)

        # Populate dish_name choices dynamically from the Dish model
        self.fields['dish_name'].choices = [
            (dish.id, dish.name) for dish in Dish.objects.all()
        ]

        # Populate new_dish_type choices from the DishType model
        self.fields['new_dish_type'].choices = [
            (dish_type.id, dish_type.name) for dish_type in DishType.objects.all()
        ]

        # Populate cook_name choices from the Cook model
        self.fields['new_cook_name'].choices = [
            (cook.id, f"{cook.first_name} {cook.last_name}") for cook in Cook.objects.all()
        ]


class DeleteDishForm(forms.Form):
    dish_name = forms.ChoiceField(
        label='Dish Name',
        choices=[],  # Initialize with an empty list, will be populated in __init__
    )

    def __init__(self, *args, **kwargs):
        super(DeleteDishForm, self).__init__(*args, **kwargs)
        # Dynamically populate dish_name choices from the updated database
        self.fields['dish_name'].choices = [
            (dish.id, dish.name) for dish in Dish.objects.all()
        ]


class GetCookForDishForm(forms.Form):
    dish_name = forms.ChoiceField(
        label='Dish Name',
        choices=[],  # Choices will be populated dynamically in __init__
    )

    def __init__(self, *args, **kwargs):
        super(GetCookForDishForm, self).__init__(*args, **kwargs)

        # Populate dish_name choices dynamically from the Dish model
        self.fields['dish_name'].choices = [
            (dish.id, dish.name) for dish in Dish.objects.all()
        ]
