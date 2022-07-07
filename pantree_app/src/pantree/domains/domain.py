import json

class Domain:
    
    def __init__(self, domain_prefix = '', re_domain_substring = '', json_file = ''):
        self.ingredients = set({})
        self.urls = set({})
        self.domain_prefix = domain_prefix
        self.re_domain_substring = re_domain_substring
        self.json_file = json_file
        with open(self.json_file,'r+') as f:
            recipes = json.load(f)
        self.urls = set(recipes.keys())


    def is_page(self):
        pass

    def get_raw_ingredient_strings(self):
        pass

    def filter_optionals(self, iterable):
        return [x for x in iterable if 'optional' not in x]

    def get_page_links_to_recipes(self):
        pass

    def get_links_to_recipes_from_homepage(self, depth = 0):
        self.get_page_links_to_recipes(URL = self.domain_prefix, depth=depth, write=True)