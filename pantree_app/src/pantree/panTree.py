import os

from .recipe import recipeDB
from . import tree


COMMON_INGS = []#['water', 'salt', 'kosher salt']

class panTree:

    def __init__(self, ingredient_list = [], must_have_list = [], 
                       db = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','recipeDB.db')):
        ingredient_list = set(ingredient_list)
        must_have_list = set(must_have_list)
        # for x in COMMON_INGS:
        #     ingredient_list.add(x)
        for x in must_have_list:
            ingredient_list.add(x)
        self.ingredient_list = [tree.find_ingredient(x) for x in ingredient_list]
        self.must_have_list = [tree.find_ingredient(x) for x in must_have_list]
        self.ingredient_list = [x for x in self.ingredient_list if x is not None]
        self.must_have_list = [x for x in self.must_have_list if x is not None]
        self.db = recipeDB(db)
        self.rank = self.db.search(self.ingredient_list, self.must_have_list)