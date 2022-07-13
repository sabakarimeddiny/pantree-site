from ..recipe import recipeDB

class Domain:
    
    def __init__(self, domain_prefix = '', re_domain_substring = '', db = ''):
        self.ingredients = set({})
        self.urls = set({})
        self.domain_prefix = domain_prefix
        self.re_domain_substring = re_domain_substring
        self.db = recipeDB(db)
    
    def is_page(self):
        pass

    def get_title(self):
        pass

    def get_time(self):
        pass

    def get_raw_ingredient_strings(self):
        pass

    def filter_optionals(self, iterable):
        return [x for x in iterable if 'optional' not in x]

    def get_page_links_to_recipes(self):
        pass

    def get_links_to_recipes_from_homepage(self, depth = 0):
        self.get_page_links_to_recipes(URL = self.domain_prefix, depth=depth)
    
    def scrape(self, depth =0):
        self.get_links_to_recipes_from_homepage(depth=depth)