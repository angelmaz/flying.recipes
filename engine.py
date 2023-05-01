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

# create lists of different types of units
weight_units = list(weights_in_g.keys())
volume_units = list(volumes_in_ml.keys())
other_units = ['', 'pinch', 'ct', 'bunch', 'slice','slices', 'stick', 'can' ]
all_units = other_units + weight_units + volume_units
# 1/2 cup = 1 stick

def convert_ingredient(ingredient, new_unit): 
    """Convert an ingredient into a new unit"""

    # create a copy of the input ingredient I don't want to modify the original
    new_ingredient = Ingredient(name=ingredient.name, quantity=ingredient.quantity, unit=ingredient.unit,
                                ingredient_id=ingredient.ingredient_id, recipe_id=ingredient.recipe_id)
    if ingredient.unit in weight_units and new_unit in weight_units:
        # convert from old unit to grams
        grams = ingredient.quantity * weights_in_g[ingredient.unit] 
        # convert from grams to the new unit
        new_ingredient.quantity = grams / weights_in_g[new_unit]
        new_ingredient.unit = new_unit
    # the same with volumes
    elif ingredient.unit in volumes_in_ml and new_unit in volumes_in_ml:
        milliliters = ingredient.quantity * volumes_in_ml[ingredient.unit]
        new_ingredient.quantity = milliliters / volumes_in_ml[new_unit]
        new_ingredient.unit = new_unit
    # if unit is the same do nothing
    elif ingredient.unit == new_unit:
        pass
    
    else:
        print(f'Cannot convert from {ingredient.unit} to {new_unit}')
        return None

    return new_ingredient

def quick_convert(quantity, unit, new_unit):
    new_quantity = None
    if unit in weight_units and new_unit in weight_units:
        # convert from old unit to grams
        grams = float(quantity) * weights_in_g[unit] 
        # convert from grams to the new unit
        new_quantity = grams / weights_in_g[new_unit]   
    # the same with volumes
    elif unit in volume_units and new_unit in volume_units:
        milliliters = float(quantity) * volumes_in_ml[unit]
        new_quantity = milliliters / volumes_in_ml[new_unit]
    # if unit is the same do nothing
    elif unit == new_unit:
        pass 
    else:
        print(f'Cannot convert from {unit} to {new_unit}')
        return None
    return new_quantity
def str_to_float(quantity_str):
    """converts quantity from str to float"""
    
    # convert empty string to none
    if quantity_str == "":
        return None
    # convert fraction 
    elif '/' in quantity_str:
        nom, denom = quantity_str.split('/')
     # if fraction > 1    
        if " " in nom:
            # split in to wholes and nominator
            a, b = nom.split(' ')
            return float(a) + float(b) / float(denom)
        else:
            return float(nom) / float(denom)
    else:
        return float(quantity_str)
