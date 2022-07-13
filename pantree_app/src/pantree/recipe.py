import os
import re
import numpy as np
from scipy.sparse import dok_matrix
import pickle
import json

from . import tree
from . import common

class Recipe:

    def __init__(self, url, ingredients):
        self.url = url
        self.ingredients = ingredients
    
    def get_ingredients(self):
        del_split = [re.split(r',|\bor,?\b|\band,?\b', x) for x in self.ingredients]
        ingredients = [x.strip() for xs in del_split for x in xs if x.strip() != '']
        #TODO: Figure out how to implement OR
        ingredients = [tree.find_ingredient(x) for x in ingredients]
        ingredients = [x for x in ingredients if x is not None]
        self.ingredients = list(set(ingredients))

    def write_recipe_to_json(self, file):
        with open(file,'r+') as f:
            try:
                data = json.load(f)
                data[self.url] = self.ingredients
            except:
                data = {}
                data[self.url] = self.ingredients
        with open(file,'w+') as f:
            json.dump(data,f)
    

class recipeBank:

    def __init__(self, json_recipe_bank = ''):
        if json_recipe_bank == '':
            self.data = None
            self.urls = None
        else:
            with open(json_recipe_bank) as json_file:
                self.recipes = json.load(json_file)
                xss = list(self.recipes.values())
                self.ingredients = sorted(set([x for xs in xss for x in xs]))
                self.urls = sorted(set(list(self.recipes.keys())))
                self.data = None
    
    def make_sparse_matrix(self):
        self.data = dok_matrix((len(self.ingredients), len(self.urls)), dtype=np.int8)
        i = 0
        urls = []
        for k, v in self.recipes.items():
            one_hot = np.array(common.vectorize(v, self.ingredients))
            one_hot_indices = np.where(one_hot == 1)
            for j in one_hot_indices:
                self.data[j, i] = 1
            i+=1
            urls.append(k)
        self.urls = urls
    
    def save(self, fname):
        with open(os.path.join(fname, 'matrix.p'), 'wb') as f:
            pickle.dump(self.data, f)
        with open(os.path.join(fname, 'urls.p'), 'wb') as f:
            pickle.dump(self.urls, f)
        with open(os.path.join(fname, 'ingredients.p'), 'wb') as f:
            pickle.dump(self.ingredients, f)
    


    
        
