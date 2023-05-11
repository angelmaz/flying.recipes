"""Kitchen-helper Flask server"""
from flask import Flask, render_template, redirect, flash, session, request, jsonify
from model import User, Recipe, Ingredient, Rating, Favorite, connect_to_db, db
import crud
import engine
from jinja2 import StrictUndefined
from sqlalchemy import delete
import os
from flask_sqlalchemy import SQLAlchemy
import fetch
from passlib.hash import argon2


app = Flask(__name__)
app.secret_key = "pascal"
app.jinja_env.undefined = StrictUndefined

app.config['UPLOAD_FOLDER'] = 'static/img/photo_recipes'
TEMP_IMG_NAME = 'temp.jpeg'
app.config['MAX_CONTENT_PATH'] = 10000000


@app.context_processor
def inject_global_vars():
    return dict(all_units=engine.all_units, weight_units=engine.weight_units, volume_units=engine.volume_units)


@app.route("/")
def index():
    """Return homepage."""
    recipes = crud.get_recipes()
    my_favorite_recipe_ids = []
    if "logged_in_user_id" in session:
        my_favorites = crud.get_favorites_by_user_id(
            session['logged_in_user_id'])
        my_favorite_recipe_ids = [
            favorite.recipe_id for favorite in my_favorites]
    return render_template("homepage.html", recipes=recipes, my_favorite_recipe_ids=my_favorite_recipe_ids)


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if not user:
        flash("No such email address, please create account")
        return redirect('/create_account')

    if not argon2.verify(password, user.password):
        flash("Incorrect password, try again.")
        return redirect("/login")

    session["logged_in_user_id"] = user.user_id
    flash("Logged in")
    return redirect("/user_dashboard")


@app.route("/create_account")
def create_account():

    return render_template("create_account.html")


@app.route("/register_user", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, argon2.hash(password))
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/login")


@app.route("/user_dashboard")
def user_dashboard():
    """Return page showing all the created and favorites recipes"""
    favorites = crud.get_favorites_by_user_id(
        user_id=session["logged_in_user_id"])
    favorite_recipes = [favorite.recipe for favorite in favorites]
    own_recipes = crud.get_recipes_by_author_id(session["logged_in_user_id"])
    my_favorite_recipe_ids = [favorite.recipe_id for favorite in favorites]

    return render_template("user_dashboard.html", favorite_recipes=favorite_recipes, own_recipes=own_recipes, my_favorite_recipe_ids=my_favorite_recipe_ids)


@app.route("/create_recipe")
def create_recipe():

    return render_template("create_recipe.html", recipe=None)

@app.route("/edit_recipe/<recipe_id>")
def edit_recipe(recipe_id):
    recipe = crud.get_recipe_by_id(recipe_id)
    return render_template("create_recipe.html", recipe=recipe)


@app.route("/recipe/<recipe_id>")
def recipe(recipe_id):
    recipe = crud.get_recipe_by_id(recipe_id)
    return render_template("recipe.html", recipe=recipe)


@app.route('/get_all_units')
def get_all_units():
    return jsonify({'all_units': engine.all_units, 'weight_units': engine.weight_units, 'volume_units': engine.volume_units})

@app.route('/save', methods=["POST"])
def save():
    ingredients = request.json.get("ingredients")
    title = request.json.get('title')
    description = request.json.get('description')
    recipe_id = request.json.get('recipe_id')
    
    create_new = False
    if recipe_id == "":
        create_new = True

    db_recipe = None
    if create_new:
        # create a new recipe
        db_recipe = crud.create_recipe_from_author_id(
            author_id=session['logged_in_user_id'], title=title, description=description, image_url='/static/img/photo_recipes/1.jpeg')
        db.session.add(db_recipe)
    else:
        # update existing recipe
        db_recipe = crud.get_recipe_by_id(recipe_id)
        db_recipe.title = title
        db_recipe.description = description
        Ingredient.query.filter_by(recipe_id=recipe_id).delete()
    
    for ingredient_dict in ingredients:
        quantity_str, unit, name = (
            ingredient_dict["quantity"],
            ingredient_dict["unit"],
            ingredient_dict["name"],
        )
        quantity = engine.str_to_float(quantity_str)
        db_ingredient = crud.create_ingredient(
            recipe=db_recipe, name=name, quantity=quantity, unit=unit)
        db.session.add(db_ingredient)

    db.session.commit()

    recipe_id = db_recipe.recipe_id
    new_file_path = f'{app.config["UPLOAD_FOLDER"]}/{recipe_id}.jpeg'
    db_recipe.image_url = f'/{new_file_path}'
    db.session.commit()
    return jsonify({"new_file_path": new_file_path})


@app.route('/convert', methods=["POST"])
def convert():
    ingredient_id = request.json.get("ingredient_id")
    unit = request.json.get('unit')
    ingredient = crud.get_ingredient_by_id(ingredient_id=ingredient_id)

    new_ingredient = engine.convert_ingredient(ingredient, unit)
    return jsonify({'quantity': new_ingredient.quantity})


@app.route('/quick_convert', methods=['POST'])
def quick_convert():
    quantity = request.json.get("quantity")
    unit = request.json.get("unit")
    new_unit = request.json.get("new_unit")

    new_quantity = engine.quick_convert(quantity, unit, new_unit)
    return jsonify({"new_quantity": new_quantity})


@app.route('/remove')
def remove():

    remove_recipe_id = request.args.get('recipe_id')
    recipe = Recipe.query.filter_by(recipe_id=remove_recipe_id).first()

    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return f'Succesfully removed recipe {remove_recipe_id}'
    else:
        return f'Cannot find recipe {remove_recipe_id} in database.'


@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        temp_file_path = f"{app.config['UPLOAD_FOLDER']}/{TEMP_IMG_NAME}"

        f = request.files['file']

        f.save(temp_file_path)
        return "STATUS: OK"
    else:
        print(f'request.method = {request.method} (not POST)')


@app.route('/rename', methods=['POST'])
def rename_file():
    if request.method == 'POST':
        current_file_path = f"{app.config['UPLOAD_FOLDER']}/{TEMP_IMG_NAME}"
        new_file_path = request.json.get('new_file_path')

        os.rename(current_file_path, new_file_path)

        flash('Great, you created and succesfully saved your recipe!')
        return "STATUS: OK"
    else:
        print(f'request.method = {request.method} (not POST)')


@app.route('/favorite_recipe')
def favorite_recipe():
    """Add recipe to favorites"""

    recipe_id = request.args.get('recipe_id')
    logged_in_user_id = session.get('logged_in_user_id')
    if logged_in_user_id is None:
        flash('You have to be logged in')
        return jsonify({'status': False})
    else:
        favorite = crud.create_favorite(logged_in_user_id, recipe_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'status': True})


@app.route('/remove_favorite_recipe')
def remove_favorite_recipe():
    recipe_id = request.args.get('recipe_id')
    logged_in_user_id = session.get('logged_in_user_id')
    if logged_in_user_id is None:
        flash('You have to be logged in')
        return jsonify({'status': False})
    else:
        favorites_to_delete = crud.get_favorite_by_user_id_and_recipe_id(
            logged_in_user_id, recipe_id)
        db.session.delete(favorites_to_delete.first())
        db.session.commit()
        return jsonify({'status': True})


@app.route('/search')
def search():
    ingredient_name = request.args.get('ingredient_name')
    if ingredient_name:
        filtered_recipes = Recipe.query.join(Recipe.ingredients).filter(
            Ingredient.name.like(f'%{ingredient_name}%')).all()
        return render_template('search.html', recipes=filtered_recipes)
    else:
        all_recipes = Recipe.query.all()
        return render_template('search.html', recipes=all_recipes)


@app.route('/web_scrapping')
def web_scrapping():
    author_id = session['logged_in_user_id']
    url = request.args.get('url')
    fetch.download_recipe(author_id, url)
    return jsonify({'status': True})


@app.route("/logout")
def process_logout():
    """Log user out."""

    del session["logged_in_user_id"]
    flash("Logged out.")
    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
