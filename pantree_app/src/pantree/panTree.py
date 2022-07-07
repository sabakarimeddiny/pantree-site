from scipy.sparse import dok_matrix
import scipy.sparse
import numpy as np

from .domains.recipe import recipeBank

from . import common


COMMON_INGS = []#['water', 'salt', 'kosher salt']

class panTree:

    def __init__(self, ingredient_list = [], recipeBank_json = ''):
        ingredient_list = set(ingredient_list)
        for x in COMMON_INGS:
            ingredient_list.add(x)
        self.ingredient_list = list(ingredient_list)
        self.data = None
        self.similarity = None
        self.difference = None
        self.rank = None
        self.bank = recipeBank(recipeBank_json)
        self.bank.make_sparse_matrix()
        
    def vectorize_ingredient_list(self):
        self.data = dok_matrix((1,len(self.bank.ingredients)), dtype=np.int8)
        one_hot = np.array(common.vectorize(self.ingredient_list, self.bank.ingredients))
        one_hot_indices = np.where(one_hot == 1)
        for j in one_hot_indices:
            self.data[0, j] = 1

    def calculate_difference(self):
        self.difference = np.zeros(self.bank.data.shape[1])
        for k, v in self.bank.data.items():
            if v == 1 and self.data[0,k[0]] == 0:
                self.difference[k[1]] += 1

    def calculate_similarity(self):
        per_url_norm = np.array(scipy.sparse.linalg.norm(self.bank.data,axis=0)).flatten()
        ing_norm = np.array(np.linalg.norm(self.data.todense()))
        self.similarity = np.array((self.data.tocsc()*self.bank.data.tocsc()).todok().todense()).flatten()/per_url_norm/ing_norm
    
    def rank_urls(self, max_missing_ings = np.inf):
        mask = np.isfinite(self.similarity)
        self.difference = np.array(self.difference)[mask]
        self.similarity = np.array(self.similarity)[mask]
        self.bank.urls = np.array(self.bank.urls)[mask]

        mask = self.difference <= max_missing_ings
        self.difference = np.array(self.difference)[mask]
        self.similarity = np.array(self.similarity)[mask]
        self.bank.urls = np.array(self.bank.urls)[mask]

        self.rank = [x for s, x in sorted(zip(self.similarity, self.bank.urls))[::-1] if s not in [0, np.nan, np.inf]]            
    
    def process(self, max_missing_ings = np.inf):
        self.vectorize_ingredient_list()
        self.calculate_difference()
        self.calculate_similarity()
        self.rank_urls(max_missing_ings)
