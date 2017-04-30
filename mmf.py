# -*- coding: utf-8 -*-

def main():
    print ("syntax:\nimport mmf\nrecipes, categories, ingredients = mmf.read_mmf(input_file)")
    
def read_mmf_file(input_filename):
    import codecs
    import re
    
    recipes = [];
    with codecs.open(input_filename,"r","ISO-8859-15") as input_file:
        #with codecs.open(output_filename, "w", "utf-8") as output_file:    
        text = input_file.read(-1)
        raw_recipes = re.findall('Title:[\s\S]+?(?=Title:)',text)
        for raw_recipe in raw_recipes:
            recipe = re.split("MMMMM[\s\S]*?[\r\n]",raw_recipe)
            recipe = ''.join(recipe)
            recipes.append(recipe)

    categories = []
    for recipe in recipes:
        line = re.findall("Categories:.*",recipe)
        raw_categories = re.findall("[\w]+(?=\r)|[\w]+(?=,)",line[0])
        categories.append(raw_categories)           
        
    ingredients = []
    for recipe in recipes:
        raw_ingredients = re.split("\n[\s]+\n",recipe)[1]
        raw_ingredients = re.split("[\s]+\n",raw_ingredients)
        ingredient_list = []
        for raw_ingredient in raw_ingredients:
            ingredient_list.append(raw_ingredient[11:])
        ingredient_list[-1] = ingredient_list[-1][:-1]
        ingredients.append(ingredient_list)
            
    return recipes, categories, ingredients

def read_mmf_dir(source_directory):
    import os
    
    recipes = []
    categories = []
    ingredients = []
    
    input_filenames = os.listdir(source_directory)
    for index, input_filename in enumerate(input_filenames):
        input_filenames[index] = source_directory + os.sep + input_filename
    
    for index, input_filename in enumerate(input_filenames):
        try:
            recipes_tmp, cat_tmp, ing_tmp = read_mmf_file(input_filename)
            if not recipes:
                recipes = recipes_tmp
                categories = cat_tmp
                ingredients = ing_tmp
            else:
                recipes.extend(recipes_tmp)
                categories.extend(cat_tmp)
                ingredients.extend(ing_tmp)
        except Exception:
            print("Error reading ", input_filename, ", skipping.")            
            
    return recipes, categories, ingredients   
    
if __name__ == "__main__":
    main()
    