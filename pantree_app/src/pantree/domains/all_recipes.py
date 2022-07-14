import re
import requests
from bs4 import BeautifulSoup
from .domain import Domain
from ..recipe import Recipe
from ..common import remove_special_char

class allRecipes(Domain):

    def __init__(self, db = ''):
        super(allRecipes, self).__init__(domain_prefix='https://www.allrecipes.com/',
                                         re_domain_substring=r'.+/recipe',
                                         db=db)
    
    def is_page(self, URL):
        if URL.startswith(self.domain_prefix + 'recipe/'):
            return True
        return False
    
    def get_title(self, URL):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("h1", class_="headline heading-content elementFont__display")[0].text.strip()
        return remove_special_char(results)

    def get_page_links_to_recipes(self, URL, depth = 0, write = True):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        links = [link for link in links if self.is_page(link)]
        for link in links:
            if self.db.check_exists(link):
                continue
            try:
                recipe = Recipe(self.get_title(link), 0, link, self.get_raw_ingredient_strings(link))
            except IndexError:
                continue
            recipe.get_ingredients()
            self.db.insert(recipe)
        depth -= 1
        if depth < 0:
            return
        else:
            for link in links:
                self.get_page_links_to_recipes(link, depth)

    def get_raw_ingredient_strings(self, URL):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("ul", class_="ingredients-section")
        ingredients = [ingredient.text.strip() for ingredient in results[0].find_all("span",class_="ingredients-item-name elementFont__body")]
        ingredients = self.filter_optionals(ingredients)
        return ingredients