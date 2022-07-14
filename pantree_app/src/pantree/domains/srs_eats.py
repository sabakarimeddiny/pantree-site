import re
import requests
from bs4 import BeautifulSoup
from .domain import Domain
from ..recipe import Recipe
from ..tree import contains_food
from ..common import remove_special_char

class srsEats(Domain):

    def __init__(self, db = ''):
        super(srsEats, self).__init__(domain_prefix='https://www.seriouseats.com/',
                                  re_domain_substring=r'https://www.seriouseats.com/',
                                  db=db)
    
    def is_page(self, URL):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div", class_="loc section-content section__content")
        try:
            results[0]
            return True
        except IndexError:
            return False
        
    def get_title(self, URL):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("h1", class_="heading__title")[0].text.strip()
        return remove_special_char(results)
    
    def get_page_links_to_recipes(self, URL, depth = 0, write = True):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        links = list(set([x for x in links if re.match(self.re_domain_substring,x) is not None]))
        links = [x for x in links if contains_food(x.split('/')[-1].replace('-','_'))]
        links = [x for x in links if self.is_page(x)]
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
        results = soup.find_all("div", class_="loc section-content section__content")
        ingredients = [ingredient.text.strip() for ingredient in results[0].find_all("span", attrs={'data-ingredient-name': True})]
        if len(ingredients) == 0:
            ingredients = [ingredient.text.strip() for ingredient in results[0].find_all("li", class_="simple-list__item js-checkbox-trigger ingredient text-passage")]
        ingredients = self.filter_optionals(ingredients)
        return ingredients



