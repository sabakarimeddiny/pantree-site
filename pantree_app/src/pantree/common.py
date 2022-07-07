
# from itertools import chain, combinations
import numpy as np

def powerset(iterable):
    # "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    # s = list(iterable)
    # return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    s = list(iterable)
    powerset = []
    # for i in range(len(s)):
    #     powerset.append([s[x] for x in range(len(s)) if x != i])
    powerset.append(iterable[1:])
    powerset.append(iterable[:-1])
    return powerset

def vectorize(ingredient_list, lex):
    return [int(x in ingredient_list) for x in lex]

def cosine_similarity(vec1, vec2):
    return np.dot(vec1,vec2)/np.linalg.norm(vec1)/np.linalg.norm(vec2)