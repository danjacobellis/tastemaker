def generate_features_and_labels():
    
    import numpy as np
    import tqdm
    
    import load_categories
    categories = load_categories.categories
    import load_dishes
    dishes = load_dishes.dishes
    if not 'recipes' in globals():
        import load_all_recipes
        recipes = load_all_recipes.load_all_recipes()
        
    all_categories = []
    for category_list in recipes['categories']:
        for category in category_list:
            all_categories.append(category)
            
    for index, category in enumerate(all_categories):
        all_categories[index] = category.replace(" ","_")
     
    from sklearn.feature_extraction.text import CountVectorizer
    count_vect = CountVectorizer()
    #variables named with 'td' are a term-doc matrix
    recipes_td = count_vect.fit_transform(all_categories)
    categories_td = count_vect.transform(categories)
    dishes_td = count_vect.transform(dishes)
    
    val, categories_ind = np.where(categories_td.sum(axis=0))
    val, dishes_ind = np.where(dishes_td.sum(axis=0))
        
    X = []
    Y = []
    for index, category_list in enumerate(recipes['categories']):
        td = count_vect.transform(category_list)
        dishes_in_recipe = np.intersect1d(td.indices, dishes_ind)
        if dishes_in_recipe.size == 0:
            continue
        categories_in_recipe = np.intersect1d(td.indices, categories_ind)
        if categories_in_recipe.size == 0:
            continue
        X.append(dishes_in_recipe)
        Y.append(categories_in_recipe)
    #    print(recipes['raw_text'][index])
    from sklearn.preprocessing import MultiLabelBinarizer
    feature_mlb = MultiLabelBinarizer()
    label_mlb = MultiLabelBinarizer()
    X = feature_mlb.fit_transform(X)
    Y = feature_mlb.fit_transform(Y)
    return X, Y

if __name__ == "__main__":
    X, Y = generate_features_and_labels()
    