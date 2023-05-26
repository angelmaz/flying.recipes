
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Data model for a users."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(30))

    def __repr__(self):
        return f"<User user_id: {self.user_id}, email: {self.email}, name: {self.name}>"

    recipes = db.relationship("Recipe", back_populates="author")
    favorites = db.relationship("Favorite", back_populates="user")
    ratings = db.relationship("Rating", back_populates="user")


class Recipe(db.Model):

    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    is_copy = db.Column(db.Boolean)
    original_recipe_id = db.Column(
        db.Integer, db.ForeignKey('recipes.recipe_id'))

    def __repr__(self):
        output = f"<Recipe recipe_id: {self.recipe_id}, author_id: {self.author_id}, title: {self.title}, is_copy: {self.is_copy}, original_recipe_id: {self.original_recipe_id}>"
        for ingredient in self.ingredients:
            output += '\n' + ingredient.__repr__()
        for paragraph in self.paragraphs:
            output += '\n' + paragraph.__repr__()
        return output

    author = db.relationship("User", back_populates="recipes")
    favorites = db.relationship(
        "Favorite", back_populates="recipe", passive_deletes=True)
    ratings = db.relationship("Rating", back_populates="recipe")
    ingredients = db.relationship(
        "Ingredient", back_populates="recipe", passive_deletes=True)
    paragraphs = db.relationship(
        "Paragraph", back_populates="recipe", passive_deletes=True)

    original_recipe = db.relationship("Recipe", back_populates="copies")
    copies = db.relationship("Recipe")


class Ingredient(db.Model):

    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        "recipes.recipe_id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Float, nullable=True)
    unit = db.Column(db.String, nullable=False)

    def __repr__(self):
        if self.quantity:
            quantity_str = f"{self.quantity:.1f}"
        else:
            quantity_str = ""
        return f"<Ingredient recipe_id: {self.recipe_id}, ingredient_id: {self.ingredient_id}, name: {self.name}, quantity: {quantity_str}, unit: {self.unit}>"

    recipe = db.relationship("Recipe", back_populates="ingredients")


class Paragraph(db.Model):

    __tablename__ = "paragraphs"

    paragraph_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        "recipes.recipe_id", ondelete="CASCADE"), nullable=False)
    text = db.Column(db.Text)

    def __repr__(self):
        return f"<Paragraph recipe_id: {self.recipe_id}, paragraph_id: {self.paragraph_id}, text: {self.text}>"

    recipe = db.relationship("Recipe", back_populates="paragraphs")


class Rating(db.Model):

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipes.recipe_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Rating rating_id: {self.rating_id}, recipe_id: {self.recipe_id}, user_id: {self.user_id}, score: {self.score}>"

    recipe = db.relationship("Recipe", back_populates="ratings")
    user = db.relationship("User", back_populates="ratings")


class Favorite(db.Model):

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipes.recipe_id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)

    def __repr__(self):
        return f"<Favorite favorite_id: {self.favorite_id}, recipe_id: {self.recipe_id}, user_id: {self.user_id}>"

    recipe = db.relationship("Recipe", back_populates="favorites")
    user = db.relationship("User", back_populates="favorites")


def connect_to_db(flask_app, db_uri="postgresql:///kitchen_helper", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
