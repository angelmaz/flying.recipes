from model import User, Recipe, Rating, Ingredient

weights_in_g = {
    'g': 1,
    'kg': 1000,
    'oz': 28.35,
    'lb': 453.6,
}

volumes_in_ml = {
    'ml': 1,
    'l': 1000,
    'tsp': 5,
    'Tbsp': 15,
    'fl oz': 30,
    'cup': 236.6,
    'gal': 3785,
}


weight_units = list(weights_in_g.keys())
volume_units = list(volumes_in_ml.keys())
other_units = ['pinch', 'ct']


def convert_ingredient(ingredient, new_unit):
    new_ingredient = Ingredient(name=ingredient.name, quantity=ingredient.quantity, unit=ingredient.unit,
                                ingredient_id=ingredient.ingredient_id, recipe_id=ingredient.recipe_id)
    if ingredient.unit in weight_units and new_unit in weight_units:
        grams = ingredient.quantity * weights_in_g[ingredient.unit]
        new_ingredient.quantity = grams / weights_in_g[new_unit]
        new_ingredient.unit = new_unit
    elif ingredient.unit in volumes_in_ml and new_unit in volumes_in_ml:
        milliliters = ingredient.quantity * volumes_in_ml[ingredient.unit]
        new_ingredient.quantity = milliliters / volumes_in_ml[new_unit]
        new_ingredient.unit = new_unit
    elif ingredient.unit == new_unit:
        pass
    else:
        print(f'Cannot convert from {ingredient.unit} to {new_unit}')
        return None

    return new_ingredient
