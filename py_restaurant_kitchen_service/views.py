from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from app.forms import DishTypeForm, CreateDishForm, UpdateDishForm, DeleteDishForm, GetCookForDishForm
from app.utils import add_dish_type, create_dish, update_dish, delete_dish, get_cook_for_dish, get_total_dish_types, get_total_dishes, count_cooks, initialize_data, create_cook
from django.views.generic import TemplateView
from django.template import TemplateDoesNotExist
from app.forms import CreateCookForm


class DeleteDishView(View):
    template_name = 'catalog/delete_dish.html'
    form_class = DeleteDishForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'message': ""})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        message = ""

        if form.is_valid():
            # Get the dish ID from the form
            dish_id = form.cleaned_data['dish_name']

            # Call the delete_dish function and get the message
            message = delete_dish(dish_id)

        return render(request, self.template_name, {'form': form, 'message': message})


class AddDishTypeView(View):
    template_name = 'catalog/dish_type.html'
    form_class = DishTypeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'message': ""})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        message = ""
        if form.is_valid():
            new_dish_type = form.cleaned_data['dish_type']
            message = add_dish_type(new_dish_type)
        return render(request, self.template_name, {'form': form, 'message': message})


class CreateDishView(View):
    template_name = 'catalog/create_dish.html'
    form_class = CreateDishForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'message': ""})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        message = ""
        if form.is_valid():
            dish_name = form.cleaned_data['dish_name']
            dish_type = form.cleaned_data['dish_type']
            cook_name = form.cleaned_data['cook_name']
            ingredients = form.cleaned_data['ingredients'].split(',')  # Convert input string to list
            price = form.cleaned_data['price']

            # Create the new dish
            message = create_dish(dish_name, dish_type, cook_name, ingredients, price)

            # Reset the form after submission
            form = self.form_class()

        return render(request, self.template_name, {'form': form, 'message': message})


class IndexView(TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Initialize context data
        context['segment'] = 'index'
        context['menu'] = initialize_data()
        context['number_of_cooks'] = count_cooks()
        context['total_dish_types'] = get_total_dish_types()
        context['total_dishes'] = get_total_dishes()

        return context


class PagesView(View):

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


class CreateCookView(View):
    template_name = 'catalog/create_cook.html'
    form_class = CreateCookForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        message = ""

        if form.is_valid():
            # Get form data, including 'years_of_experience'
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            years_of_experience = form.cleaned_data['years_of_experience']  # Make sure this is included

            # Call the create_cook method with the correct arguments
            message = create_cook(username, email, first_name, last_name, years_of_experience)

        return render(request, self.template_name, {'form': form, 'message': message})


class UpdateDishView(View):
    template_name = 'catalog/update_dish.html'
    form_class = UpdateDishForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'message': ""})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        message = ""

        if form.is_valid():
            # Extract form data
            dish_id = form.cleaned_data['dish_name']
            new_dish_name = form.cleaned_data.get('new_dish_name')
            new_dish_type = form.cleaned_data.get('new_dish_type')
            new_cook_name = form.cleaned_data.get('new_cook_name')
            new_ingredients = form.cleaned_data.get('new_ingredients')
            price = form.cleaned_data.get('price')

            # Call the update_dish function and get the result message
            message = update_dish(
                dish_name=dish_id,
                new_dish_name=new_dish_name,
                new_dish_type=new_dish_type,
                new_cook_name=new_cook_name,
                new_ingredients=new_ingredients,
                price=price
            )

        return render(request, self.template_name, {'form': form, 'message': message})


class GetCookForDishView(View):
    template_name = 'catalog/get_cook_for_dish.html'
    form_class = GetCookForDishForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'message': ""})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        message = ""

        if form.is_valid():
            # Get the selected dish ID from the form
            dish_id = form.cleaned_data['dish_name']

            # Call get_cook_for_dish function with the dish ID
            message = get_cook_for_dish(dish_id)

        return render(request, self.template_name, {'form': form, 'message': message})