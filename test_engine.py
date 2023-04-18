from engine import convert_ingredient
import seed_database

print(f'before conversion: {seed_database.ingredient1}')

ingredient1_converted = convert_ingredient(seed_database.ingredient1, 'l')
print(f'after conversion {ingredient1_converted}')