from model import db, User, Recipe, Rating, Ingredient, Favorite, Paragraph, connect_to_db


def create_user(email, password, name):
    """Create and return a new user."""

    user = User(email=email, password=password, name=name)
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


def create_recipe(author, title, image_url, is_copy=False, original_recipe_id=None):
    """Create and return a new recipe."""

    recipe = Recipe(
        author=author,
        title=title,
        image_url=image_url,
        is_copy=is_copy,
        original_recipe_id=original_recipe_id
    )
    return recipe


def create_recipe_from_author_id(author_id, title, image_url, is_copy=False, original_recipe_id=None):

    recipe = Recipe(
        author_id=author_id,
        title=title,
        image_url=image_url,
        is_copy=is_copy,
        original_recipe_id=original_recipe_id
    )
    return recipe


def get_recipes():
    """Return all recipes"""

    return Recipe.query.all()


def get_recipe_by_id(recipe_id):
    """Return a recipe by primary key"""

    return Recipe.query.get(recipe_id)


def get_recipes_by_author_id(author_id):
    return Recipe.query.filter(Recipe.author_id == author_id)


def create_ingredient(recipe, name, quantity, unit):
    """Create and return new ingredient"""

    ingredient = Ingredient(recipe=recipe, name=name,
                            quantity=quantity, unit=unit)
    return ingredient


def get_ingredient_by_id(ingredient_id):
    return Ingredient.query.get(ingredient_id)

def create_paragraph(recipe, text):
    """Create and return new paragraph"""

    paragraph = Paragraph(recipe=recipe, text=text)
    return paragraph

def create_favorite(user_id, recipe_id):
    """Create and return favorite recipe"""

    favorite = Favorite(user_id=user_id, recipe_id=recipe_id)
    return favorite


def get_favorite_by_id(favorite_id):
    """Get favorite recipe by id"""

    return Favorite.query.get(favorite_id)

def get_favorites_by_user_id(user_id):
    """return list of favorite recipes"""
    return Favorite.query.filter(Favorite.user_id == user_id)

def get_favorite_by_user_id_and_recipe_id(user_id, recipe_id):
    return Favorite.query.filter(Favorite.user_id == user_id, Favorite.recipe_id == recipe_id)

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
