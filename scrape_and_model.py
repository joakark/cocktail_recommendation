# import necassary libraries

import pandas as pd
import numpy as np

import requests
from requests.auth import HTTPBasicAuth
import string
import warnings

warnings.filterwarnings("ignore")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import matplotlib.pyplot as plt

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


def get_ingredients(cocktail_dict):

  # pulls the ingredients of each cocktail (that are stored in 'strIngredient1', 'strIngredient2' etc) in one string

    ingredient = cocktail_dict['strIngredient1']
    i = 2

    ingredient_list = ""

    while ingredient:

        ingredient_list = ingredient + ", " + ingredient_list
        ingredient = cocktail_dict['strIngredient'+str(i)]

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
                cocktail['ingredients'] = get_ingredients(cocktail_list[i]['drinks'][j])
                cocktail['instructions'] = cocktail_list[i]['drinks'][j]['strInstructions']

                cocktails_info.append(cocktail)
        except:
            pass   #ignore cocktails for which there is no data

    return cocktails_info



cocktails_info = cocktail_data_clean(cocktail_list)


# #### Step 2: Find cocktail similarity using Tf-idf vectorizer and cosine similarity of the ingredients

cocktail_df = pd.DataFrame(cocktails_info)


def similar_cocktail(cocktail_df, chosen_cocktail):

    # string pre-processing
    cocktail_df['drink'] = cocktail_df['drink'].str.lower().str.replace('[^\w\s]','')
    cocktail_df['ingredients'] = cocktail_df['ingredients'].str.lower().str.replace('[^\w\s]','')
    cocktail_df['instructions'] = cocktail_df['instructions'].str.lower().str.replace('[^\w\s]','')

    # implement tf-idf vectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(cocktail_df['ingredients'])
    arr = X.toarray()

    similarity_table = pd.DataFrame(cosine_similarity(arr), columns=cocktail_df['drink'], index=cocktail_df['drink'])
    
    for column in similarity_table.columns:
            similarity_table[column] = np.where(similarity_table[column] >= 1, 0, similarity_table[column])
        
    similar_cocktail= similarity_table.idxmax()
    
    try:
        new_cocktail = similar_cocktail[chosen_cocktail][0]
    except:
        new_cocktail = similar_cocktail[chosen_cocktail].unique()[0]

    return new_cocktail
