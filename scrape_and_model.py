# import necassary libraries

import pandas as pd
import numpy as np
import requests
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_url_list():

    # gets the url for each potential first letter of a cocktail name - a,b,c.. 1,2,.. etc and stores them in a list

    url_list = []
    main_url = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?f='

    for i in string.printable:
        url_list.append(main_url+i)

    return url_list


def scrape_cocktail_list():

  # scrapes the information for a list of url's

    cocktail_list = []
    url_list = get_url_list()

    for i in url_list:
        try:
            r = requests.get(i, verify=False)
            cocktail_list.append(r.json())
        except:
            pass
    return cocktail_list


cocktail_list = scrape_cocktail_list()

# create columns that show ingredients and their quantity

for i in range(len(cocktail_list)):
    try:
        for j in range(len(cocktail_list[i]['drinks'])):
            for k in range(1,16):
                if cocktail_list[i]['drinks'][j]['strIngredient'+str(k)] is not None:
                    try:
                        cocktail_list[i]['drinks'][j]['ingredient_and_quantity'+str(k)] = cocktail_list[i]['drinks'][j]['strIngredient'+str(k)] + " - " + cocktail_list[i]['drinks'][j]['strMeasure'+str(k)]
                    except:
                        cocktail_list[i]['drinks'][j]['ingredient_and_quantity'+str(k)] = cocktail_list[i]['drinks'][j]['strIngredient'+str(k)] 
                else:
                    cocktail_list[i]['drinks'][j]['ingredient_and_quantity'+str(k)] = None
    except:
        pass



def get_ingredients(cocktail_dict, col_name):

  # pulls the ingredients of each cocktail (that are stored in 'strIngredient1', 'strIngredient2' etc) in one string

    ingredient = cocktail_dict[col_name + '1']
    i = 2

    ingredient_list = ""

    while ingredient:

        ingredient_list = ingredient + ", " + ingredient_list
        ingredient = cocktail_dict[col_name + str(i)]

        i = i+1

    return ingredient_list


def cocktail_data_clean(cocktail_list):

    # creates a list of dictionaries, one for each cocktail with the information of interest

    cocktails_info = []

    for i in range(len(cocktail_list)):
        try:
            for j in range(len(cocktail_list[i]['drinks'])):
                cocktail = {}
                cocktail['drink'] = cocktail_list[i]['drinks'][j]['strDrink']
                cocktail['ingredients'] = get_ingredients(cocktail_list[i]['drinks'][j],'strIngredient')
                cocktail['ingredients_and_quantities'] = get_ingredients(cocktail_list[i]['drinks'][j],'ingredient_and_quantity')
                cocktail['instructions'] = cocktail_list[i]['drinks'][j]['strInstructions']

                cocktails_info.append(cocktail)
        except:
            pass   #ignore cocktails for which there is no data

    return cocktails_info



cocktails_info = cocktail_data_clean(cocktail_list)


# #### Step 2: Find cocktail similarity using Tf-idf vectorizer and cosine similarity of the ingredients

cocktail_df = pd.DataFrame(cocktails_info)
cocktail_df.drop_duplicates(inplace=True)


def similar_cocktail(cocktail_df, chosen_cocktail):

    # string pre-processing
    cocktail_df['ingredients_processed'] = cocktail_df['ingredients'].str.lower().str.replace('[^\w\s]','')

    # implement tf-idf vectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(cocktail_df['ingredients_processed'])
    arr = X.toarray()

    similarity_table = pd.DataFrame(cosine_similarity(arr), columns=cocktail_df['drink'], index=cocktail_df['drink'])
    
    for column in similarity_table.columns:
            similarity_table[column] = np.where(similarity_table[column] >= 1, 0, similarity_table[column])
        
    similar_cocktail= similarity_table.idxmax()
    
    new_cocktail = similar_cocktail[chosen_cocktail]

    return new_cocktail
