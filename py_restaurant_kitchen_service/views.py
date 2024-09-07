
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from app.forms import DishTypeForm, CreateDishForm, UpdateDishForm, DeleteDishForm, GetCookForDishForm
from app.utils import add_dish_type, create_dish, update_dish, delete_dish, get_cook_for_dish, get_total_dish_types, get_total_dishes, count_cooks, initialize_data


def get_cook_for_dish_view(request):
    message = ""
    if request.method == 'POST':
        form = GetCookForDishForm(request.POST)
        if form.is_valid():
            dish_name = form.cleaned_data['dish_name']
            message = get_cook_for_dish(dish_name)
            return render(request, 'catalog/get_cook_for_dish.html', {'form': form, 'message': message})
    else:
        form = GetCookForDishForm()

    return render(request, 'catalog/get_cook_for_dish.html', {'form': form, 'message': message})


def delete_dish_view(request):
    message = ""
    if request.method == 'POST':
        form = DeleteDishForm(request.POST)
        if form.is_valid():
            dish_name = form.cleaned_data['dish_name']
            message = delete_dish(dish_name)

            # Redirect to a success page or a list of dishes after deletion
            return render(request, 'catalog/delete_dish.html', {'form': form, 'message': message})
    else:
        form = DeleteDishForm()

    return render(request, 'catalog/delete_dish.html', {'form': form, 'message': message})


def update_dish_view(request):
    message = ""
    if request.method == 'POST':
        form = UpdateDishForm(request.POST)
        if form.is_valid():
            dish_name = form.cleaned_data['dish_name']
            new_dish_name = form.cleaned_data.get('new_dish_name')
            new_dish_type = form.cleaned_data.get('new_dish_type')
            new_cook_name = form.cleaned_data.get('new_cook_name')
            new_ingredients = form.cleaned_data.get('new_ingredients')
            price = form.cleaned_data.get('price')

            message = update_dish(
                dish_name,
                new_dish_name=new_dish_name,
                new_dish_type=new_dish_type,
                new_cook_name=new_cook_name,
                new_ingredients=new_ingredients.split(',') if new_ingredients else None,
                price=price
            )
            form = UpdateDishForm()
            return render(request, 'catalog/update_dish.html', {'form': form, 'message': message})
    else:
        form = UpdateDishForm()

    return render(request, 'catalog/update_dish.html', {'form': form, 'message': message})


def add_dish_type_view(request):
    message = ""
    if request.method == 'POST':
        form = DishTypeForm(request.POST)
        if form.is_valid():
            new_dish_type = form.cleaned_data['dish_type']
            message = add_dish_type(new_dish_type)
            return render(request, 'catalog/dish_type.html', {'form': form, 'message': message})
    else:
        form = DishTypeForm()

    return render(request, 'catalog/dish_type.html', {'form': form, 'message': message})


def create_dish_view(request):
    message = ""
    if request.method == 'POST':
        form = CreateDishForm(request.POST)
        if form.is_valid():
            dish_name = form.cleaned_data['dish_name']
            dish_type = form.cleaned_data['dish_type']
            cook_name = form.cleaned_data['cook_name']
            ingredients = form.cleaned_data['ingredients'].split(',')  # Convert input string to list
            price = form.cleaned_data['price']

            message = create_dish(dish_name, dish_type, cook_name, ingredients, price)
            form = CreateDishForm()  # Reset the form after submission
    else:
        form = CreateDishForm()

    return render(request, 'catalog/create_dish.html', {'form': form, 'message': message})


#@login_required(login_url="/login/")
def index(request):

    menu = initialize_data()

    number_of_cooks = count_cooks()

    total_dish_types = get_total_dish_types()

    total_dishes = get_total_dishes()

    context = {'segment': 'index', "total_dish_types": total_dish_types, "total_dishes": total_dishes, "number_of_cooks": number_of_cooks, "menu": menu}

    html_template = loader.get_template('catalog/index.html')
    return HttpResponse(html_template.render(context, request))


#@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('catalog/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('catalog/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('catalog/page-500.html')
        return HttpResponse(html_template.render(context, request))
