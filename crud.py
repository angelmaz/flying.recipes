from model import db, User, Recipe, Rating, Ingredient, Favorite, Paragraph, connect_to_db

# users


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


# recipes

def add_recipe(author, title, image_url, is_copy=False, original_recipe_id=None):
    """Create and return a new recipe."""

    recipe = Recipe(
        author=author,
        title=title,
        image_url=image_url,
        is_copy=is_copy,
        original_recipe_id=original_recipe_id
    )

    db.session.add(recipe)
    db.session.commit()

    if is_copy == False:
        recipe.original_recipe_id = recipe.recipe_id
    db.session.commit()

    return recipe


def add_recipe_from_author_id(author_id, title, image_url, is_copy=False, original_recipe_id=None):

    recipe = Recipe(
        author_id=author_id,
        title=title,
        image_url=image_url,
        is_copy=is_copy,
        original_recipe_id=original_recipe_id
    )

    db.session.add(recipe)
    db.session.commit()

    if is_copy == False:
        recipe.original_recipe_id = recipe.recipe_id
    db.session.commit()

    return recipe


def get_recipes():
    """Return all recipes"""

    return Recipe.query.all()


def get_recipe_by_id(recipe_id):
    """Return a recipe by primary key"""

    return Recipe.query.get(recipe_id)


def get_original_recipes():
    return Recipe.query.filter(Recipe.is_copy == False)


def get_copies_of_author_id(author_id):
    return Recipe.query.filter(Recipe.is_copy == True, Recipe.author_id == author_id)


def get_recipes_to_show(author_id):
    favorite_recipes = get_copies_of_author_id(author_id)
    originals_to_skip = [r.original_recipe_id for r in favorite_recipes]
    filtered_originals = Recipe.query.filter(
        Recipe.is_copy == False, Recipe.recipe_id not in originals_to_skip)

    return filtered_originals + favorite_recipes


def original_recipe_ids_liked_by(author_id):
    copies = get_copies_of_author_id(author_id)
    liked_original_ids = [r.original_recipe_id for r in copies]
    return liked_original_ids

def authored_recipe_ids(author_id):
    authored_recipes = Recipe.query.filter(Recipe.author_id == author_id, Recipe.is_copy == False)
    return [r.recipe_id for r in authored_recipes]

def get_recipes_by_author_id(author_id):
    return Recipe.query.filter(Recipe.author_id == author_id)


def get_copy_from_original_id(original_recipe_id, author_id):
    copies = Recipe.query.filter(
        Recipe.author_id == author_id, Recipe.original_recipe_id == original_recipe_id)
    return get_recipe_by_id(copies.first().recipe_id)


def add_copy_from_recipe_id(recipe_id, author_id):
    original_recipe = get_recipe_by_id(recipe_id)
    copy = add_recipe_from_author_id(
        author_id=author_id, title=original_recipe.title,
        image_url=original_recipe.image_url, is_copy=True,
        original_recipe_id=recipe_id)

    original_paragraphs = Paragraph.query.filter(
        Paragraph.recipe_id == recipe_id)
    for paragraph in original_paragraphs:
        new_paragraph = create_paragraph(recipe=copy, text=paragraph.text)
        db.session.add(new_paragraph)

    original_ingredients = Ingredient.query.filter(
        Ingredient.recipe_id == recipe_id)
    for ingredient in original_ingredients:
        new_ingredient = create_ingredient(
            recipe=copy, name=ingredient.name, quantity=ingredient.quantity,
            unit=ingredient.unit)
        db.session.add(new_ingredient)

    db.session.commit()


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
