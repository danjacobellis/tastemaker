# -*- coding: utf-8 -*-
import mmf
import os
import numpy as np
import re

#input_filename = 'recipes' + os.sep + '10000.mmf'
#recipes, categories, ingredients = mmf.read_mmf_file(input_filename)
source_directory = "." + os.sep + "recipes"
recipes, categories, ingredients = mmf.read_mmf_dir(source_directory)


#--------------------------------ingredients-----------------------------------
all_ingredients = []
for ingredient_list in ingredients:
    for ingredient in ingredient_list:
        all_ingredients.append(ingredient)
        
for index, ingredient in enumerate(all_ingredients):
    all_ingredients[index] = ingredient.replace(" ","_")
 
from sklearn.feature_extraction.text import CountVectorizer
count_vect_ing = CountVectorizer()
#term_doc_ing = count_vect_ing.fit_transform(all_ingredients).toarray()
term_doc_ing = count_vect_ing.fit_transform(all_ingredients)
#inv_trans = count_vect_ing.inverse_transform(term_doc_ing)

num_unique_ing = np.shape(term_doc_ing)[1]
num_ing = np.shape(term_doc_ing)[0]
print("there are", num_unique_ing, "unique ingredients out of",num_ing)

import matplotlib.pyplot as plt
#ingredient_freq = np.sum(term_doc_ing, axis=0)
ingredient_freq = np.asarray( term_doc_ing.sum(axis=0) )[0]
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
keep_term_doc = np.zeros((num_keep,num_unique_ing))
for ind, val in enumerate(top_ind):
    keep_term_doc[ind,val] = 1
labels = count_vect_ing.inverse_transform(keep_term_doc)
freqs = ingredient_freq[top_ind]

print("Most common ingredients:\n", labels)
print("Number of occurances:\n",freqs)

#--------------------------------ingredients-----------------------------------
all_categories = []
for category_list in categories:
    for category in category_list:
        all_categories.append(category)
        
for index, category in enumerate(all_categories):
    all_categories[index] = category.replace(" ","_")
 
from sklearn.feature_extraction.text import CountVectorizer
count_vect_cat = CountVectorizer()
term_doc_cat = count_vect_cat.fit_transform(all_categories).toarray()
inv_trans = count_vect_cat.inverse_transform(term_doc_cat)

num_unique_cat = np.shape(term_doc_cat)[1]
num_cat= np.shape(term_doc_cat)[0]
print("there are", num_unique_cat, "unique categories out of",num_cat)

import matplotlib.pyplot as plt
category_freq = np.sum(term_doc_cat, axis=0)
sorted_category_freqs = np.flipud(np.argsort(category_freq))

fig = plt.figure()
fig.add_axes()
ax1 = plt.gca()
ax1.set_yscale('log')
ax1.set_xscale('log')
plt1 = plt.plot(category_freq[sorted_category_freqs])
plt.xlabel('Category Index')
plt.ylabel('Number of Occurances of Category')

num_keep = 25
top_ind = sorted_category_freqs[0:num_keep]
keep_term_doc = np.zeros((num_keep,num_unique_cat))
for ind, val in enumerate(top_ind):
    keep_term_doc[ind,val] = 1
labels = count_vect_cat.inverse_transform(keep_term_doc)
freqs = category_freq[top_ind]

print("Most common categories:", labels,freqs)








