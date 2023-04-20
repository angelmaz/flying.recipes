from model import db, User, Recipe, Rating, Ingredient, Favorite, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)
    return user


def get_users():
    """Return all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def create_recipe(author, title, description):
    """Create and return a new recipe."""

    recipe = Recipe (
        author=author,
        title=title,
        description=description,
        )
    return recipe


def get_recipes():
    """Return all recipes"""

    return Recipe.query.all()


def get_recipe_by_id(recipe_id):
    """Return a recipe by primary key"""
    
    return Recipe.query.get(recipe_id)


def create_ingredient(recipe, name, quantity, unit):
    """Create and return new ingredient"""
    
    ingredient = Ingredient(recipe=recipe, name=name, quantity=quantity, unit=unit)
    return ingredient


def create_favorite(recipe, user):
    """Create and return favorite recipe"""
    
    favorite = Favorite(recipe=recipe, user=user)
    return favorite

def get_favorite_by_id(favorite_id):
    """Get favorite recipe by id"""

    return Favorite.query.get(favorite_id)


def create_rating(user, recipe, score):
    """Create and return a new rating."""

    rating = Rating(user=user, recipe=recipe, score=score)
    return rating


def update_rating(rating_id, new_score):
    """ Update a rating given rating_id and the updated score. """
    
    rating = Rating.query.get(rating_id)
    rating.score = new_score


if __name__ == "__main__":
    from server import app

    connect_to_db(app)