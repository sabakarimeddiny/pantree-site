import re
import sqlite3

from . import tree

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
        self.cur.execute("CREATE VIRTUAL TABLE recipes USING FTS5(title, time, url, ingredients)")
    
    def insert(self, recipe):
        self.cur.execute("INSERT INTO recipes VALUES (?,?,?,?)",
                         (recipe.title, recipe.time, recipe.url, recipe.ingredients))
        self.save()

    def count(self):
        self.cur.execute("SELECT Count() FROM recipes")
        return self.cur.fetchone()[0]
    
    def search(self, ingredient_list, must_have_list):
        query = "SELECT title, url FROM recipes "
        if ingredient_list != [] or must_have_list != []:
            query += "WHERE ingredients MATCH '("
            if ingredient_list != []:
                query += " OR ".join(ingredient_list) + ")"
                if must_have_list != []:
                    query += " AND ("
                else:
                    query += "'"
            query += " AND ".join(must_have_list) 
            if must_have_list != []:
                query += ")'"
            query += " ORDER BY bm25(recipes)"
        print(query)
        return self.cur.execute(query).fetchall()
        
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
        


    
        
