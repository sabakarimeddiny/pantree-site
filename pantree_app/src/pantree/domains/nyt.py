import re
import requests
import json
from bs4 import BeautifulSoup
from .domain import Domain
from ..recipe import Recipe

class NYT(Domain):

    def __init__(self, db = ''):
        super(NYT, self).__init__(domain_prefix='https://cooking.nytimes.com',
                                  re_domain_substring=r'/recipes/\d+',
                                  db=db)
    
    def is_page(self, URL):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("section", id="error")
        try:
            b = 'Page Not Found' in results[0].find_all("h1")[0]
        except IndexError:
            return True
        return not b
    
    def get_title(self, URL):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("h1", class_="contenttitle_contentTitle__36j2i header_recipe-name__PkKYu")[0].text.strip()
        return results

    def get_time(self):
        pass

    def get_page_links_to_recipes(self, URL, depth = 0):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        links = list(set([x for x in links if re.match(self.re_domain_substring,x) is not None]))
        links = [self.domain_prefix + x for x in links]
        links = [link.split('?')[0] for link in links if self.is_page(link)]
        for link in links:
            if self.db.check_exists(link):
                continue
            recipe = Recipe(self.get_title(link), 0, link, self.get_raw_ingredient_strings(link))
            recipe.get_ingredients()
            self.db.insert(recipe)
        depth -= 1
        if depth < 0:
            return
        else:
            for link in links:
                self.get_page_links_to_recipes(link, depth)

    def get_raw_ingredient_strings(self, URL):
        ingredients = []
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div", class_="recipe-instructions")
        if results != []:
            ingredients = [ingredient.text.strip() for ingredient in results[0].find_all("span",class_="ingredient-name")]
        else:
            ingredients =json.loads(soup.find_all('script')[0].text)['recipeIngredient']
            ingredients = [x.split('\xa0')[0] for x in ingredients]      
        ingredients = self.filter_optionals(ingredients)
        return ingredients

