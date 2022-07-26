import os
import datetime
import re
from queue import Queue
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

nltk.data.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'nltk_data'))
# from transformers import pipeline
# from transformers import AutoTokenizer, AutoModelForTokenClassification

# tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
# model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
# nlp = pipeline("ner", model=model, tokenizer=tokenizer)

from .common import powerset

def txt_2_list(file):
    list_from_file = []
    with open(file) as f:
        lines = f.readlines()
        for l in lines:
            list_from_file.append(l.strip())
    return list_from_file

def txt_2_dict(file):
    dict_from_file = {}
    with open(file) as f:
        lines = f.readlines()
        for l in lines:
            dict_from_file[l.split(':')[0].strip()] = l.split(':')[1].strip()
    return dict_from_file


lexicon_edit_path = os.path.join(os.path.dirname(__file__), '..', 'lexicon_edit')
ADD_FOODS = txt_2_list(os.path.join(lexicon_edit_path,'add_foods.txt'))
SUBTRACT_FOODS = txt_2_list(os.path.join(lexicon_edit_path,'subtract_foods.txt'))
SUB_DICT = txt_2_dict(os.path.join(lexicon_edit_path,'substitute_words.txt'))


lm = nltk.stem.wordnet.WordNetLemmatizer()

def is_food(word):
    if word in ADD_FOODS:
        return 1
    elif word in SUBTRACT_FOODS:
        return 0
    syns = wn.synsets(str(word), pos = wn.NOUN)
    for syn in syns:
        if 'food' in syn.lexname():
            return 1
        # elif 'substance' in syn.lexname():
        #     return 1
    if '_' in word:
        return int(0 not in [is_food(x) for x in word.split('_')])
    if '_cheese' in word:
        return is_food(word.replace('_cheese',''))

    return 0

def contains_food(word):
    return int(sum([is_food(x) for x in word.split('_')]) > 0) or is_food(word)

def is_unit(word):
    syns = wn.synsets(str(word), pos = wn.NOUN)
    for syn in syns:
        if 'quantity' in syn.lexname():
            return 1
    return 0

def clean_ing_string(string):
    string = re.sub(r"\((.*?)\)", "", string)
    string = re.sub(r'[^\w\s]', '', string)
    string = string.lower()
    raw = word_tokenize(string)
    lemmatized = [lm.lemmatize(i) for i in raw]
    subbed = []
    for word in lemmatized:
        if word in list(SUB_DICT.keys()):
            subbed.append(SUB_DICT[word])
        else:
            subbed.append(word)
    return '_'.join(subbed)


class Tree:
    def __init__(self, data, parent = None):
        self.data = data
        self.words = len(data.split('_'))
        self.children = []
        self.parent = parent
        if parent is None:
            self.unique_children = {data}
        self.start_time = datetime.datetime.now().time()

    def get_head(self):
        if self.parent is None:
            return self
        else:
            return self.parent.get_head()

    def add_child(self, data):
        self.children.append((Tree(data, parent = self)))
        
    def generate_children(self):
        if self.words == 1:
            return
        current_time = datetime.datetime.now().time()
        if (current_time.minute*60 + current_time.second) - (self.get_head().start_time.minute*60 + self.get_head().start_time.second) > 15:
            return
        children = ['_'.join(x) for x in list(powerset(self.data.split('_')))]
        children = [x for x in children if contains_food(x)]
        [self.add_child(x) for x in children if x not in self.get_head().unique_children]
        [self.get_head().unique_children.add(x) for x in children]
        [x.generate_children() for x in self.children]

    def level_order(self):
        Q = Queue()
        level_ordered_foods = []
        Q.put(self)
        while (not Q.empty()):
            node = Q.get()
            if node == None:
                continue
            level_ordered_foods.append(node.data)
            [Q.put(x) for x in node.children]
        return list(pd.unique(level_ordered_foods))
            
    def find_highest_food(self):
        for x in self.level_order():
            if is_food(x):
                return ' '.join(x.split('_'))


def find_ingredient(string):
    string = clean_ing_string(string)
    string = ' '.join(string.split('_'))
    return string
    # head = Tree(clean_ing_string(string))
    # head.generate_children()
    # ing = head.find_highest_food()
    # if ing == 'clove' and 'garlic' in string: #put this into a separate lex edit file
    #     return 'garlic'
    # else:
    #     return ing

    



