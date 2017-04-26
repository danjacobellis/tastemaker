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
    
if __name__ == "__main__":
    main()
    