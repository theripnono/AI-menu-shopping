# server/test/test_generate_recipes.py
import unittest
import os
import sys

#Saber en qué directorio estoy
current_directory = os.getcwd()
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from generate_recipes import GenerateRecipes

class TestGenerateRecipes(unittest.TestCase):

    def test_template_menu(self):
        generator = GenerateRecipes()
        categories_context = "category1, category2"


if __name__ == '__main__':
    unittest.main()