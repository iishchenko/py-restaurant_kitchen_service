from django.contrib import admin
from app.models import DishType, Ingredient, Cook, Dish

admin.site.register(DishType)
admin.site.register(Ingredient)
admin.site.register(Cook)
admin.site.register(Dish)

