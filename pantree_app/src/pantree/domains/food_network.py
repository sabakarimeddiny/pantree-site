import re
import requests
from bs4 import BeautifulSoup
from .domain import Domain
from ..recipe import Recipe

class foodNetwork(Domain):

    def __init__(self, json_file = ''):
        super(foodNetwork, self).__init__(domain_prefix='https://www.foodnetwork.com/recipes/',
                                  re_domain_substring=r'.+/recipes',
                                  json_file=json_file)
    
    def is_page(self, URL):
        if URL.endswith('.recipePrint'):
            return False
        if URL.startswith(self.domain_prefix):
            return True
        return False
    
    def get_page_links_to_recipes(self, URL, depth = 0, write = True):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        links = list(set([x for x in links if re.match(self.re_domain_substring,x) is not None]))
        links = ['https:' + x for x in links]
        links = [link for link in links if self.is_page(link)]
        if write:
            for link in links:
                if link in self.urls:
                    continue
                try:
                    recipe = Recipe(link, self.get_raw_ingredient_strings(link))
                except IndexError:
                    continue
                recipe.get_ingredients()
                recipe.write_recipe_to_json(self.json_file)
        else:
            [self.urls.add(x) for x in links]
        depth -= 1
        if depth < 0:
            return
        else:
            for link in links:
                self.get_page_links_to_recipes(link, depth)

    def get_raw_ingredient_strings(self, URL):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div", class_="o-Ingredients__m-Body")
        ingredients = [ingredient.text.strip() for ingredient in results[0].find_all("span",class_="o-Ingredients__a-Ingredient--CheckboxLabel")]
        ingredients = [x.split('\n')[-1] for x in ingredients]
        ingredients = self.filter_optionals(ingredients)
        ingredients = [x for x in ingredients if x != 'Deselect All']
        return ingredients