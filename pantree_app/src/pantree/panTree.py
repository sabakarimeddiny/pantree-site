from scipy.sparse import dok_matrix
import scipy.sparse
import numpy as np

from .domains.recipe import recipeBank

from . import common


COMMON_INGS = ['water', 'salt', 'kosher salt']

class panTree:

    def __init__(self, ingredient_list = [], recipeBank_json = ''):
        ingredient_list = set(ingredient_list)
        for x in COMMON_INGS:
            ingredient_list.add(x)
        self.ingredient_list = list(ingredient_list)
        self.data = None
        self.similarity = None
        self.rank = None
        self.bank = recipeBank(recipeBank_json)
        self.bank.make_sparse_matrix()
        
    def vectorize_ingredient_list(self):
        self.data = dok_matrix((1,len(self.bank.ingredients)), dtype=np.int8)
        one_hot = np.array(common.vectorize(self.ingredient_list, self.bank.ingredients))
        one_hot_indices = np.where(one_hot == 1)
        for j in one_hot_indices:
            self.data[0, j] = 1

    def calculate_similarity(self):
        per_url_norm = np.array(scipy.sparse.linalg.norm(self.bank.data,axis=0)).flatten()
        ing_norm = np.array(np.linalg.norm(self.data.todense()))
        self.similarity = np.array((self.data.tocsc()*self.bank.data.tocsc()).todok().todense()).flatten()/per_url_norm/ing_norm
    
    def rank_urls(self):
        mask = np.isfinite(self.similarity)
        masked_similarity = np.array(self.similarity)[mask]
        masked_urls = np.array(self.bank.urls)[mask]
        self.rank = [x for s, x in sorted(zip(masked_similarity, masked_urls))[::-1] if s not in [0, np.nan, np.inf]]
    
    def process(self):
        self.vectorize_ingredient_list()
        self.calculate_similarity()
        self.rank_urls()
