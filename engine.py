from model import User, Recipe, Rating, Ingredient

def convert_ingredient(ingredient, new_unit):

    if ingredient.unit == 'ml' and new_unit == 'l':
        ingredient.unit = 'l'
        ingredient.quantity /= 1000
    else:
        print('curently we only convert from ml to l')
    
    return ingredient

