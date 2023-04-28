"""Kitchen-helper Flask server"""
from flask import Flask, render_template, redirect, flash, session, request, jsonify
from model import User, Recipe, Ingredient, Rating, Favorite, connect_to_db, db
import crud
import engine
from jinja2 import StrictUndefined
from sqlalchemy import delete
import os


app = Flask(__name__)
app.secret_key = "pascal"
app.jinja_env.undefined = StrictUndefined

app.config['UPLOAD_FOLDER'] = 'static/img/photo_recipes'
TEMP_IMG_NAME = 'temp.jpeg'
app.config['MAX_CONTENT_PATH'] = 10000000


@app.route("/")
def index():
    """Return homepage."""
    recipes = crud.get_recipes()
    return render_template("homepage.html", recipes=recipes)


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

    if user.password != password:
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
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/login")


@app.route("/user_dashboard")
def user_dashboard():
    """Return page showing all the created and favorites recipes"""

    recipes_author = crud.get_recipes_by_author_id(
        session["logged_in_user_id"])
    recipe_list = crud.get_favorite_by_id
    return render_template("user_dashboard.html", recipe_list=recipe_list, recipes=recipes_author)


@app.route("/create_recipe")
def create_recipe():

    return render_template("create_recipe.html", all_units=engine.all_units)


@app.route("/recipe/<recipe_id>")
def recipe(recipe_id):
    recipe = crud.get_recipe_by_id(recipe_id)
    return render_template("recipe.html", recipe=recipe, weight_units=engine.weight_units, volume_units=engine.volume_units)


@app.route('/get_all_units')
def get_all_units():
    return jsonify({'all_units': engine.all_units})


@app.route('/save', methods=["POST"])
def save():
    ingredients = request.json.get("ingredients")
    title = request.json.get('title')
    description = request.json.get('description')
    db_recipe = crud.create_recipe_from_author_id(
        author_id=session['logged_in_user_id'], title=title, description=description, image_url='/static/img/photo_recipes/1.jpeg')
    db.session.add(db_recipe)
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
    return jsonify({'quantity':new_ingredient.quantity})

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


@app.route("/logout")
def process_logout():
    """Log user out."""

    del session["logged_in_user_id"]
    flash("Logged out.")
    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

# @app.route('/user_dashboard/<favorite_by_id>')
# def favorite_by_id(favorite_id):
#     favorite_by_id = crud.get_favorite_by_id(favorite_id)
#     return render_template('user_dashboard.html', favorite_by_id=favorite_by_id)
