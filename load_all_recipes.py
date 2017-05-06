def load_all_recipes():
    import mmf
    import os
    import numpy as np
    import re
    
    #input_filename = 'recipes' + os.sep + '10000.mmf'
    #recipes, categories, ingredients = mmf.read_mmf_file(input_filename)
    source_directory = "." + os.sep + "recipes"
    recipes, categories, ingredients = mmf.read_mmf_dir(source_directory)
    recipes = {'raw_text':recipes, 'categories':categories, 'ingredients':ingredients}
    return recipes

if __name__ == "__main__":
    recipes = load_all_recipes()