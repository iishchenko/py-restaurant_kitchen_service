"""
URL configuration for py_restaurant_kitchen_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from py_restaurant_kitchen_service import views

urlpatterns = [
                  # The home page
                  path('', views.index, name='home'),  # Ensure 'index' view exists in views.py

                  # Route for adding dish type
                  path('dish_type/', views.add_dish_type_view, name='dish_type'),

                  path('create_dish/', views.create_dish_view, name='create_dish'),

                  path('update_dish/', views.update_dish_view, name='update_dish'),

                  path('delete_dish/', views.delete_dish_view, name='delete_dish'),

                  path('get_cook_for_dish/', views.get_cook_for_dish_view, name='get_cook_for_dish'),

                  path(r'^.*\.*', views.pages, name='pages'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
