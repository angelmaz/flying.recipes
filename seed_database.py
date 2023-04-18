"""Script to seed database."""

import os
from random import choice, randint
from model import db, User, Recipe, Rating, Ingredient, connect_to_db
import crud
from flask import Flask
app = Flask(__name__)


# We are using os.system to automatically dropdb for us
os.system("dropdb kitchen_helper")
os.system('createdb kitchen_helper')
#connect to the database by calling db.create_all
connect_to_db(app)
db.create_all()


email = 'user@test.com'
password = 'test'

user = crud.create_user(email, password)
db.session.add(user)

recipe = crud.create_recipe(author=user, title='buleczki', description='do pieca')
db.session.add(recipe)

ingredient1 = crud.create_ingredient(recipe= recipe, name="milk", quantity=500, unit='ml')
db.session.add(ingredient1)
db.session.commit()

