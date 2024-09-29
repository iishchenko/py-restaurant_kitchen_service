from django.db import models
from django.contrib.auth.models import AbstractUser


class DishType(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=255)


class Cook(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    years_of_experience = models.IntegerField()


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    cooks = models.ManyToManyField(Cook,  related_name='dish')
    ingredients = models.ManyToManyField(Ingredient, related_name='dishes')

    def __str__(self):
        return self.name
