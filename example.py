# -*- coding: utf-8 -*-
import mmf
import os
import numpy as np
import re

input_filename = 'recipes' + os.sep + '10000.mmf'

recipes, categories, ingredients = mmf.read_mmf_file(input_filename)

all_ingredients = []
for ingredient_list in ingredients:
    for ingredient in ingredient_list:
        all_ingredients.append(ingredient)
        
for index, ingredient in enumerate(all_ingredients):
    all_ingredients[index] = ingredient.replace(" ","_")
#    for match in re.finditer(' ', ingredient):
#        ingredient[ma

    
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
term_doc_matrix = count_vect.fit_transform(all_ingredients).toarray()
inv_trans = count_vect.inverse_transform(term_doc_matrix)

num_unique = np.shape(term_doc_matrix)[1]
num_ingredients = np.shape(term_doc_matrix)[0]
print("there are", num_unique, "unique ingredients out of",num_ingredients)

import matplotlib.pyplot as plt
ingredient_freq = np.sum(term_doc_matrix, axis=0)
sorted_ingredient_freqs = np.flipud(np.argsort(ingredient_freq))

fig = plt.figure()
fig.add_axes()
ax1 = plt.gca()
ax1.set_yscale('log')
ax1.set_xscale('log')
plt1 = plt.plot(ingredient_freq[sorted_ingredient_freqs])
plt.xlabel('Ingredient Index')
plt.ylabel('Number of Occurances of Ingredient')

num_keep = 25
top_ind = sorted_ingredient_freqs[0:num_keep]
keep_term_doc = np.zeros((num_keep,num_unique))
for ind, val in enumerate(top_ind):
    keep_term_doc[ind,val] = 1
labels = count_vect.inverse_transform(keep_term_doc)
freqs = ingredient_freq[top_ind]

print("Most common ingredients:", labels,freqs)








