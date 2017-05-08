def generate_features_and_labels():
    import load_categories
    categories = load_categories.categories
    categories.sort()
    import load_dishes
    dishes = load_dishes.dishes
    dishes.sort()
    
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
    num_categories = np.shape(recipes_td)[1]
    
    val, categories_ind = np.where(categories_td.sum(axis=0) == 1)
    val, dishes_ind = np.where(dishes_td.sum(axis=0) == 1)
        
    X = []
    Y = []
    recipes_used = []
    print("encoding features and lablels...")
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
        recipes_used.append(
                {'raw_text':recipes['raw_text'][index],
                 'categories':recipes['categories'][index], 
                 'ingredients':recipes['ingredients'][index]})
    #    print(recipes['raw_text'][index])
    from sklearn.preprocessing import MultiLabelBinarizer
    feature_mlb = MultiLabelBinarizer().fit(X)
    label_mlb = MultiLabelBinarizer().fit(Y)
    X_t = feature_mlb.transform(X)
    Y_t = label_mlb.transform(Y)
    
    missing_dishes_ind = np.setdiff1d(dishes_ind,feature_mlb.classes_)    
    num_missing_dishes = np.shape(missing_dishes_ind)[0]
    missing_dishes_td = sp.sparse.csr_matrix((num_missing_dishes,num_categories))
    for i in range(num_missing_dishes):
        j = missing_dishes_ind[i]
        missing_dishes_td[i,j] = 1
    missing_dishes = count_vect.inverse_transform(missing_dishes_td)
    
    missing_categories_ind = np.setdiff1d(categories_ind, label_mlb.classes_)
    num_missing_categories = np.shape(missing_categories_ind)[0]
    missing_categories_td = sp.sparse.csr_matrix((num_missing_categories,num_categories))
    for i in range(num_missing_categories):
        j = missing_categories_ind[i]
        missing_categories_td[i,j] = 1
    missing_categories = count_vect.inverse_transform(missing_categories_td)
    
    dishes_ind = np.setdiff1d(dishes_ind, missing_dishes_ind)
    categories_ind = np.setdiff1d(categories_ind, missing_categories_ind)
    
    print("ignoring:\n",missing_dishes,missing_categories)
    
    p = dishes_ind.size
    q = categories_ind.size
    
    feature_mapping = sp.sparse.csr_matrix((p,num_categories))
    for i in range(p):
        j = dishes_ind[i]
        feature_mapping[i,j] = 1
    label_mapping = sp.sparse.csr_matrix((q,num_categories))
    for i in range(q):
        j = categories_ind[i]
        label_mapping[i,j] = 1
                     
    dishes_str = count_vect.inverse_transform(feature_mapping)
    categories_str = count_vect.inverse_transform(label_mapping)
    return X_t, Y_t, dishes_str, categories_str, recipes_used, feature_mapping, label_mapping

def train_multi_label_classifier(X,Y):
    n,q = np.shape(Y)
    models = []
#    for label in tqdm(range(1)):
    for label in tqdm(range(q)):
        y = Y[:,label]
        model = train_single_label_classifier(X,y)
        models.append(model)
        import os
        model_filename = (os.getcwd() + os.sep + 'models' + os.sep \
                          + str(label).zfill(3) + "dish_to_category_xgb.model")
        model.save_model(model_filename)
    return models

def train_single_label_classifier(X,y):
    dtrain = xgb.DMatrix(X,label=y)
    param = {'objective':'binary:logistic','nthread':4,
             'nfold':10,'max_depth':8}
#    xgb.cv(params = param, dtrain = dtrain, metrics={'error'}, seed = 0,
#       callbacks=[xgb.callback.print_evaluation(show_stdv=True)])
    model = xgb.train(params = param, dtrain = dtrain)
#    model = xgb.XGBClassifier(max_depth = 8, nthread = 4).fit(X, y)
    return model
    
def eval_accuracy(models, X_test, Y_test, operating_point):
    num_test_samples = np.shape(X_test)[0]
    dtest = xgb.DMatrix(X_test)
    preds = np.zeros(np.shape(Y_test))
    offset = operating_point - 0.5
    for index, model in enumerate(models):
        preds[:,index] = np.round(model.predict(dtest) + offset)
    plt.figure(1, figsize=(28, 2))
    plt.imshow(preds.T)
    plt.ylabel('Category')
    plt.xlabel('Test Sample Index')
    plt.title('Model Predictions')
    
    plt.figure(2, figsize=(28, 2))
    plt.imshow(Y_test.T)
    plt.ylabel('Category')
    plt.xlabel('Test Sample Index')
    plt.title('True Test Labels')
    num_tp = 0
    num_fp = 0
    num_tn = 0
    num_fn = 0
    tp = []
    fp = []
    tn = []
    fn = []

    for i in range(num_test_samples):
        model_true = np.where(preds[i,:] == 1)
        model_false = np.where(preds[i,:] == 0)
        data_true = np.where(Y_test[i,:] == 1)
        data_false = np.where(Y_test[i,:] == 0)
        tp.append(np.intersect1d(data_true,model_true))
        fp.append(np.setdiff1d(data_true,model_true))
        tn.append(np.intersect1d(data_false, model_false))
        fn.append(np.setdiff1d(data_false,model_false))
        num_tp += tp[-1].size
        num_fp += fp[-1].size
        num_tn += tn[-1].size
        num_fn += fn[-1].size
#    accuracy = (num_tp + num_tn) / (num_tp + num_tn + num_fp + num_fn)
    accuracy = (num_tp + num_tn) / (num_tp + num_fp)
    print("\naccuracy:", accuracy)
    return accuracy, tp, num_tp, fp, num_fp, tn, num_tn, fn, num_fn    

def predict_from_pretrained_models(top5_str, top5_proba):
    import numpy as np
    import xgboost as xgb
    import os
    
    dishes_str = np.load("dishes_str.npy")
    categories_str = np.load("categories_str.npy")
    feature_mapping = np.load("feature_mapping.npy")
    label_mapping = np.load("label_mapping.npy")
    
    models = [];
    for index, category in enumerate(categories_str):
        bst = xgb.Booster({'nthread':4})
        model_filename = (os.getcwd() + os.sep + 'models' + os.sep \
                          + str(index).zfill(3) + "dish_to_category_xgb.model")
        model = bst.load_model(model_filename)
        models.append(model)   
    
if __name__ == "__main__":
    import numpy as np
    import scipy as sp
    import matplotlib.pyplot as plt
    import xgboost as xgb
    from tqdm import tqdm
    
    if not 'X' in globals():
        X, Y, dishes_str, categories_str, recipes_used, \
        feature_mapping, label_mapping \
        = generate_features_and_labels()
        np.save("dishes_str.npy", dishes_str)
        np.save("categories_str.npy", categories_str)
        np.save("feature_mapping.npy", feature_mapping)
        np.save("label_mapping.npy", label_mapping)
    print("done encoding features and labels")
    
    print("example of data format:\n")
    print(">>recipes_used[0]['raw_text']")
    print(recipes_used[0]['raw_text'])
    print(">>dishes_str[np.where(X[0,:])[0][0]]")
    print(dishes_str[np.where(X[0,:])[0][0]])
    print(">>categories_str[np.where(Y[0,:])[0][0]]")
    print(categories_str[np.where(Y[0,:])[0][0]])
        
    n, p = np.shape(X)
    n, q = np.shape(Y)
    
#    models were trained with 90-10 split
#    split = int(np.round(0.1*n))

#    only show half of the test data
    split = int(np.round(0.05*n))
    
    X_test = X[:split,:]
    Y_test = Y[:split,:]
    X_train = X[split:,:]
    Y_train = Y[split:,:]
    
    if not 'models' in globals():
        models = train_multi_label_classifier(X_train,Y_train)
    
    accuracy, tp, num_tp, fp, num_fp, tn, num_tn, fn, num_fn \
    = eval_accuracy(models, X_test, Y_test, 0.7)
    
    
    
    
    