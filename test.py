import unittest
from model import Ingredient
from engine import to_canonical, convert_ingredient, quick_convert, str_to_float


class TestConversionFunctions(unittest.TestCase):
    def test_to_canonical(self):
        self.assertEqual(to_canonical('kg'), 'kg')
        self.assertEqual(to_canonical('kilograms'), 'kg')
        self.assertEqual(to_canonical('tbsp'), 'Tbsp')
        self.assertIsNone(to_canonical('foo'))

    def test_convert_ingredient(self):
        ing1 = Ingredient(name='flour', quantity=1, unit='lb',
                          ingredient_id=1, recipe_id=1)
        ing2 = Ingredient(name='flour', quantity=16,
                          unit='oz', ingredient_id=1, recipe_id=1)
        self.assertEqual(convert_ingredient(
            ing1, 'oz').quantity, ing2.quantity)
        self.assertIsNone(convert_ingredient(ing1, 'ml'))

    def test_quick_convert(self):
        self.assertAlmostEqual(quick_convert(1, 'lb', 'oz'), 16)
        self.assertAlmostEqual(quick_convert(1, 'tsp', 'ml'), 5)
        self.assertIsNone(quick_convert(1, 'lb', 'ml'))

    def test_str_to_float(self):
        self.assertEqual(str_to_float('1/2'), 0.5)
        self.assertEqual(str_to_float('3 1/2'), 3.5)
        self.assertEqual(str_to_float(''), None)
        self.assertEqual(str_to_float('1.5'), 1.5)
