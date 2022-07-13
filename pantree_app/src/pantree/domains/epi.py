import re
import requests
from bs4 import BeautifulSoup
from .domain import Domain
from ..recipe import Recipe

class epicurious(Domain):

    def __init__(self, db = ''):
        super(epicurious, self).__init__(domain_prefix='https://www.epicurious.com/recipes/',
                                         re_domain_substring=r'.+/recipes',
                                         db=db)
    
    def is_page(self, URL):
        if URL.startswith(self.domain_prefix):
            return True
        return False
    
    def get_title(self, URL):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("h1", class_="BaseWrap-sc-TURhJ BaseText-fFzBQt SplitScreenContentHeaderHed-fxVOKs eTiIvU gaogNm fOuMTo")[0].text.strip()
        return results
    
    def get_page_links_to_recipes(self, URL, depth = 0, write = True):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        fixed_links = []
        for link in links:
            if link.startswith('/recipes/'):
                fixed_links.append('https://www.epicurious.com' + link)
            if link.startswith(self.domain_prefix):
                fixed_links.append(link)
        links = fixed_links
        # links = list(set([x for x in links if re.match(self.re_domain_substring,x) is not None]))
        links = [link.split('#')[0] for link in links if self.is_page(link)]
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
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div", class_="BaseWrap-sc-TURhJ BaseText-fFzBQt Description-dSNklj eTiIvU feJvcP cZDSEe")
        ingredients = [ingredient.text.strip() for ingredient in results]
        ingredients = [x.split('\n')[-1] for x in ingredients]
        ingredients = self.filter_optionals(ingredients)
        return ingredients