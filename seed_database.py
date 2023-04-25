"""Script to seed database."""
import json
import os
from random import choice, randint
from model import db, User, Recipe, Rating, Ingredient, Favorite, connect_to_db
import crud
import server
from flask import Flask
from engine import str_to_float
app = Flask(__name__)


# os.system to automatically dropdb for us
os.system("dropdb kitchen_helper")
os.system('createdb kitchen_helper')
# connect to the database by calling db.create_all
connect_to_db(server.app, echo=False)
db.create_all()


# take one user in loop with his parameters from json, and add to db
with open('data/users.json') as f:
    user_data = json.loads(f.read())

users_in_db = []
for user in user_data:
    email, password = (
        user["email"],
        user["password"],
    )
    db_user = crud.create_user(email=email, password=password)
    users_in_db.append(db_user)

db.session.add_all(users_in_db) # add all users to db

# take recipe in a loop from json and add to db
with open('data/recipes.json') as f:
    recipe_data = json.loads(f.read())

for recipe in recipe_data:
    author_id, title, ingredients_dicts, description, image_url = (
        recipe["author_id"],
        recipe["title"],
        recipe["ingredients"],
        recipe["description"],
        recipe["image_url"],
    )
    db_recipe = crud.create_recipe_from_author_id(
        author_id=author_id, title=title, description=description, image_url=image_url)
    db.session.add(db_recipe)
    for ingredient_dict in ingredients_dicts:
        quantity_str, unit, name = (
            ingredient_dict["quantity"],
            ingredient_dict["unit"],
            ingredient_dict["name"],
        )
        quantity = str_to_float(quantity_str)
        db_ingredient = crud.create_ingredient(recipe=db_recipe, name=name, quantity=quantity, unit=unit)
        db.session.add(db_ingredient)

db.session.commit()

