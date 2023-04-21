"""Kitchen-helper Flask server"""
from flask import Flask, render_template, redirect, flash, session, request
from model import User, Recipe, Ingredient, Rating, Favorite, connect_to_db, db
import crud
import engine
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "pascal"
app.jinja_env.undefined = StrictUndefined

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

    session["logged_in_user_email"] = user.email
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
    
    recipe_list = crud.get_favorite_by_id
    return render_template("user_dashboard.html", recipe_list=recipe_list)

@app.route("/create_recipe")
def create_recipe():

    return render_template("create_recipe.html")

@app.route("/recipe/<recipe_id>")
def recipe(recipe_id):
    recipe = crud.get_recipe_by_id(recipe_id)
    return render_template("recipe.html", recipe=recipe)

@app.route("/logout")
def process_logout():
    """Log user out."""

    del session["logged_in_user_email"]
    flash("Logged out.")
    return redirect("/")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
