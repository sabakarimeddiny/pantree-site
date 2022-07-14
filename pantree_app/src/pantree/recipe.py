import os
import re
import sqlite3
import pickle
import json
import numpy as np
from scipy.sparse import dok_matrix

from . import tree
from . import common

class Recipe:

    def __init__(self, title, time, url, ingredients):
        self.title = title
        self.time = time
        self.url = url
        self.ingredients = ingredients
    
    def get_ingredients(self):
        del_split = [re.split(r',|\bor,?\b|\band,?\b', x) for x in self.ingredients]
        ingredients = [x.strip() for xs in del_split for x in xs if x.strip() != '']
        ingredients = [tree.find_ingredient(x) for x in ingredients]
        ingredients = [x for x in ingredients if x is not None]
        self.ingredients = ','.join(list(set(ingredients)))

class recipeDB:

    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.ingredients = set({})

    def create_table(self):
        self.cur.execute('''CREATE TABLE recipes
                            (title text, time real, url text, ingredients text)''')
    
    def insert(self, recipe):
        self.cur.execute("INSERT INTO recipes VALUES (?,?,?,?)",
                         (recipe.title, recipe.time, recipe.url, recipe.ingredients))
        self.save()

    def count(self):
        self.cur.execute("SELECT Count() FROM recipes")
        return self.cur.fetchone()[0]
        
    def get_ingredients(self):
        for ingredients in self.cur.execute('SELECT ingredients FROM recipes'):
            [self.ingredients.add(x) for x in ingredients[0].split(',')]
        self.ingredients = sorted(self.ingredients)

    def serialize(self, dir_):
        titles = []
        times = []
        urls = []
        matrix = dok_matrix((len(self.ingredients), self.count()), dtype=np.int8)
        i = 0
        for row in self.cur.execute('SELECT * FROM recipes'):
            title = row[0]
            time = row[1]
            url = row[2]
            ingredients = row[3].split(',')
            one_hot = np.array(common.vectorize(ingredients, self.ingredients))
            one_hot_indices = np.where(one_hot == 1)
            for j in one_hot_indices:
                matrix[j, i] = 1
            i+=1
            titles.append(title)
            times.append(time)
            urls.append(url)

        with open(os.path.join(dir_, 'titles.p'), 'wb') as f:
            pickle.dump(titles, f)
        with open(os.path.join(dir_, 'matrix.p'), 'wb') as f:
            pickle.dump(matrix, f)
        with open(os.path.join(dir_, 'urls.p'), 'wb') as f:
            pickle.dump(urls, f)
        with open(os.path.join(dir_, 'ingredients.p'), 'wb') as f:
            pickle.dump(self.ingredients, f)
        

    def check_exists(self, url):
        self.cur.execute("SELECT url FROM recipes WHERE url=?", (url,))
        result = self.cur.fetchone()
        if result:
            return True
        else:
            return False

    def save(self):
        self.con.commit()

    def close(self):
        self.con.close()
    
    def clear(self):
        self.cur.execute("DROP TABLE recipes")
 

class recipeBank:

    def __init__(self):
        self.data = None
        self.urls = None
        self.titles = None
        self.ingredients = None
        


    
        
