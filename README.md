# py-restaurant_kitchen_service


This Django application is designed to manage a system where cooks can create new dishes, categorize them into types, and assign specific cooks to prepare each dish. The system also allows for managing ingredients and their associations with dishes. 

## Features

- **Dish Management:** Create and manage dishes, including assigning cooks responsible for each dish.
- **Dish Types:** Define and manage various types of dishes for better organization.
- **Ingredient Management:** Add and manage ingredients, with a many-to-many relationship to dishes.
- **Dynamic Forms:** Update dishes through forms with dropdown lists of existing dish names.

## Installation 

Python3 must be already installed

'''shell

git clone https://github.com/iishchenko/py-restaurant_kitchen_service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver

'''