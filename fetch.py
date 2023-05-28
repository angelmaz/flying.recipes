import requests
from bs4 import BeautifulSoup
from engine import str_to_float, to_canonical
import crud
from model import db


def ingredient_from_text(text):
    tokens = text.split(" ")
    name_index = 0
    quantity = None
    unit = None
    if tokens[0].isdigit() or "/" in tokens[0]:
        if '/' in tokens[1]:
            quantity = str_to_float(tokens[0] + " " + tokens[1])
            unit_index = 2
        else:
            quantity = str_to_float(tokens[0])
            unit_index = 1

        unit = to_canonical(tokens[unit_index])
        if unit is None:
            name_index = unit_index
        else:
            name_index = unit_index + 1

    name = ' '.join(tokens[name_index:])
    if not unit:
        unit = ""
    return {'quantity': quantity, 'unit': unit, 'name': name, }


def download_recipe(author_id, url):
    """Downloads recipe from foodnetwork.com"""

    data = requests.get(url)
    html = BeautifulSoup(data.text, 'html.parser')

    img = html.select('img.m-MediaBlock__a-Image')[0]
    img_src = 'https://' + img.get('src')[2:]

    title = html.select('span.o-AssetTitle__a-HeadlineText')[0]
    title_text = title.decode_contents()

    descriptions_list = html.select('div.o-Method__m-Body')
    descriptions = descriptions_list[0].select('li')
    description_text_list = []
    for description in descriptions:
        description_text = description.decode_contents()
        description_text_list.append(description_text)
    recipe = crud.add_recipe_from_author_id(
        author_id=author_id, title=title_text, image_url=img_src)

    for text in description_text_list:
        db_paragraph = crud.create_paragraph(recipe=recipe, text=text)
        db.session.add(db_paragraph)
    ingredients = html.select('p.o-Ingredients__a-Ingredient')
   
    for ingredient in ingredients[1:]:
        ingredient_text = ingredient.select(
            '.o-Ingredients__a-Ingredient--CheckboxLabel')[0].get_text()
        ingredient_dict = ingredient_from_text(ingredient_text)
        db_ingredient = crud.create_ingredient(
            recipe=recipe, name=ingredient_dict['name'], quantity=ingredient_dict['quantity'], unit=ingredient_dict['unit'])
        db.session.add(db_ingredient)
    db.session.commit()
