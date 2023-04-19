from engine import convert_ingredient, scale_recipe
import seed_database



ingredient1_fl_oz = convert_ingredient(seed_database.ingredient1, 'fl oz')
print(f'before conversion: {seed_database.ingredient1}')
print(f'after conversion to fl oz: {ingredient1_fl_oz}')

ingredient2_converted = convert_ingredient(seed_database.ingredient2, 'oz')
print(f'before conversion: {seed_database.ingredient2}')
print(f'after conversion to oz: {ingredient2_converted}')


ingredient3_converted = convert_ingredient(seed_database.ingredient3, 'ct')
print(f'before conversion: {seed_database.ingredient3}')
print(f'after conversion to ct: {ingredient3_converted}')

recipe_scaled = scale_recipe(seed_database.recipe, 1.5)
print(f'recipe before scaling: {seed_database.recipe}')
print(f'recipe after scaling: {recipe_scaled}')