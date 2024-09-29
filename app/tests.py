from django.test import TestCase
from app.models import Dish, DishType, Cook, Ingredient
from decimal import Decimal


class DishModelTest(TestCase):

    def setUp(self):
        self.dish_type = DishType.objects.create(name="Appetizer")
        self.cook = Cook.objects.create(username="chef1", years_of_experience=5)  # Додано years_of_experience
        self.ingredient = Ingredient.objects.create(name="Tomato")

    def test_create_dish(self):
        dish = Dish.objects.create(
            name="Tomato Soup",
            dish_type=self.dish_type,
            price=5.99
        )
        dish.cooks.add(self.cook)
        dish.ingredients.add(self.ingredient)

        self.assertEqual(dish.name, "Tomato Soup")
        self.assertEqual(dish.dish_type, self.dish_type)
        self.assertEqual(dish.price, 5.99)
        self.assertIn(self.cook, dish.cooks.all())
        self.assertIn(self.ingredient, dish.ingredients.all())


class DishUpdateTest(TestCase):

    def setUp(self):
        self.dish_type = DishType.objects.create(name="Main Course")
        self.cook = Cook.objects.create(username="chef2", years_of_experience=10)
        self.dish = Dish.objects.create(
            name="Grilled Chicken",
            dish_type=self.dish_type,
            price=Decimal('12.99')  # Використовуйте Decimal для ціни
        )
        self.dish.cooks.add(self.cook)

    def test_update_dish(self):
        self.dish.name = "Grilled Chicken with Herbs"
        self.dish.price = Decimal('14.99')  # Використовуйте Decimal для ціни
        self.dish.save()

        self.dish.refresh_from_db()  # Оновіть об'єкт з бази даних

        self.assertEqual(self.dish.name, "Grilled Chicken with Herbs")
        self.assertEqual(self.dish.price, Decimal('14.99'))  # Порівняння з Decimal


class DishDeletionTest(TestCase):

    def setUp(self):
        self.dish_type = DishType.objects.create(name="Dessert")
        self.cook = Cook.objects.create(username="chef3", years_of_experience=7)  # Додано years_of_experience
        self.dish = Dish.objects.create(
            name="Chocolate Cake",
            dish_type=self.dish_type,
            price=4.99
        )
        self.dish.cooks.add(self.cook)

    def test_delete_dish(self):
        dish_id = self.dish.id
        self.dish.delete()

        with self.assertRaises(Dish.DoesNotExist):
            Dish.objects.get(id=dish_id)


class GetCookForDishTest(TestCase):

    def setUp(self):
        self.dish_type = DishType.objects.create(name="Salad")
        self.cook = Cook.objects.create(username="chef4", years_of_experience=3)  # Додано years_of_experience
        self.dish = Dish.objects.create(
            name="Caesar Salad",
            dish_type=self.dish_type,
            price=7.99
        )
        self.dish.cooks.add(self.cook)

    def test_get_cook_for_dish(self):
        cooks = self.dish.cooks.all()
        self.assertIn(self.cook, cooks)
        self.assertEqual(cooks.count(), 1)
