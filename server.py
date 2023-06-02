"""Kitchen-helper Flask server"""
from flask import Flask, render_template, redirect, flash, session, request, jsonify
from model import User, Recipe, Ingredient, Rating, Favorite, Paragraph, connect_to_db, db
import crud
import engine
from jinja2 import StrictUndefined
from sqlalchemy import delete
import os
from flask_sqlalchemy import SQLAlchemy
import fetch
from passlib.hash import argon2
import mailtrap as mt
import jwt
import time

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
    recipes_to_show = crud.get_original_recipes()
    
    liked_recipe_ids = []
    authored_recipe_ids = []
    if "logged_in_user_id" in session:
        liked_recipe_ids = crud.original_recipe_ids_liked_by(session['logged_in_user_id'])
        authored_recipe_ids = crud.authored_recipe_ids(session['logged_in_user_id'])
    return render_template("homepage.html", recipes_to_show=recipes_to_show, liked_recipe_ids=liked_recipe_ids, authored_recipe_ids=authored_recipe_ids)


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html", hide_quick=True)


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
    session['logged_in_email'] = user.email
    session['logged_in_name'] = user.name
    flash("Logged in")
    return redirect("/user_dashboard")


@app.route("/create_account")
def create_account():

    return render_template("create_account.html", hide_quick=True)


@app.route("/register_user", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, argon2.hash(password), name)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/login")


@app.route("/user_dashboard")
def user_dashboard():
    """Return page showing all the created and favorites recipes"""
    
    own_recipes = crud.get_recipes_by_author_id(session["logged_in_user_id"])
   
    return render_template("user_dashboard.html", own_recipes=own_recipes)


@app.route("/create_recipe")
def create_recipe():

    return render_template("create_recipe.html", recipe=None)


@app.route("/edit_recipe/<recipe_id>")
def edit_recipe(recipe_id):
    recipe = crud.get_recipe_by_id(recipe_id)
    return render_template("create_recipe.html", recipe=recipe)


@app.route("/recipe/<recipe_id>")
def recipe(recipe_id):
    recipe_id = int(recipe_id)
    recipe = crud.get_recipe_by_id(recipe_id)
    if "logged_in_user_id" in session:
        copies = crud.get_copies_of_author_id(session['logged_in_user_id'])
        for r in copies:
            if r.original_recipe_id == recipe_id:
                recipe = r
    return render_template("recipe.html", recipe=recipe)


@app.route('/get_all_units')
def get_all_units():
    return jsonify({'all_units': engine.all_units, 'weight_units': engine.weight_units, 'volume_units': engine.volume_units})


@app.route('/save', methods=["POST"])
def save():
    ingredients = request.json.get("ingredients")
    title = request.json.get('title')
    paragraphs = request.json.get('paragraphs')
    recipe_id = request.json.get('recipe_id')
    file_input = request.json.get('file_input')

    create_new = False
    if recipe_id == "":
        create_new = True

    db_recipe = None
    if create_new:
        # create a new recipe
        db_recipe = crud.add_recipe_from_author_id(
            author_id=session['logged_in_user_id'], title=title, image_url='/static/img/YourDish.png')
    else:
        # update existing recipe
        db_recipe = crud.get_recipe_by_id(recipe_id)
        db_recipe.title = title
        Ingredient.query.filter_by(recipe_id=recipe_id).delete()
        Paragraph.query.filter_by(recipe_id=recipe_id).delete()

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

    for text in paragraphs:
        db_paragraph = crud.create_paragraph(recipe=db_recipe, text=text)
        db.session.add(db_paragraph)

    db.session.commit()

    recipe_id = db_recipe.recipe_id

    new_file_path = f'{app.config["UPLOAD_FOLDER"]}/{recipe_id}.jpeg'

    if file_input:
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

    logged_in_user_id = session.get('logged_in_user_id')
    if logged_in_user_id is None:
        flash('You have to be logged in')
        return jsonify({'status': False})
    else:
        copy_recipe_id = request.args.get('copy_recipe_id')
        original_recipe_id = None
        if not copy_recipe_id:
            original_recipe_id = int(request.args.get('original_recipe_id'))
        else:
            original_recipe_id = crud.get_recipe_by_id(int(copy_recipe_id)).original_recipe_id

        crud.add_copy_from_recipe_id(
            recipe_id=original_recipe_id, author_id=logged_in_user_id)
        return jsonify({'status': True})


@app.route('/remove_favorite_recipe')
def remove_favorite_recipe():
    if 'logged_in_user_id' not in session:
        flash('You have to be logged in')
        return jsonify({'status': False})
    else:
        logged_in_user_id = session.get('logged_in_user_id')
        copy_recipe_id = request.args.get('copy_recipe_id')

        copy_to_delete = None
        if not copy_recipe_id:    
            original_recipe_id = request.args.get('original_recipe_id')
            copy_to_delete = crud.get_copy_from_original_id(
                original_recipe_id=original_recipe_id, author_id=logged_in_user_id)
        else:
            copy_to_delete = crud.get_recipe_by_id(copy_recipe_id)

        db.session.delete(copy_to_delete)
        db.session.commit()
        return jsonify({'status': True})


@app.route('/search')
def search():
    ingredient_name = request.args.get('ingredient_name')
    if ingredient_name:
        filtered_recipes = Recipe.query.join(Recipe.ingredients).filter(
            Ingredient.name.ilike(f'%{ingredient_name}%')).all()
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

    del session['logged_in_user_id']
    del session['logged_in_email']
    del session['logged_in_name']
    flash("Logged out.")
    return redirect("/")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/send_email", methods=["POST"])
def send_email():
    def get_reset_token(email, expires=500):
        return jwt.encode(
                {'reset_password': email, 'exp': time.time() + expires},
                key=os.getenv('SECRET_KEY_FLASK'),
                algorithm='HS256')

    email = request.form.get('email')
    token = get_reset_token(email)

    mail = mt.Mail(
        sender=mt.Address(email="no-reply@flying.recipes", name="Mailtrap Test"),
        to=[mt.Address(email=email)],
        subject="You are awesome!",
        text=(f"Congrats for sending test email. Your token is:\n" 
            + f"http://flying.recipes/reset_password?email={email}&token={token}"))

    client = mt.MailtrapClient(token=os.getenv('MT_TOKEN'))
    client.send(mail)
    flash("Password recovery email has been sent.")
    return redirect("/login")

@app.route("/reset_password")
def reset_password():
    email = request.args.get('email')
    token = request.args.get('token')
    print(f"email: '{email}', token: '{token}'")

    # print(f"token decoded: '{token.decode('utf-8')}'")

    try:
        decoded_email = jwt.decode(token, key=os.getenv('SECRET_KEY_FLASK'), 
                algorithms=['HS256'])['reset_password']
        if decoded_email == email:
            flash("email and token matches")
            return render_template("reset_password.html", email=email)
        else:
            flash("email and token do not match!")
            return redirect("/login")
    except Exception as e:
        flash(f"Exception during token decoding: {e}")
        return redirect("/login")

@app.route("/set_password", methods=['POST'])
def set_password():
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    user.password = argon2.hash(password)
    db.session.add(user)
    db.session.commit()

    return render_template("login.html", hide_quick=True)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
