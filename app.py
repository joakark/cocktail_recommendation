import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app=Flask(__name__)

## Load the model and perform transformations
cocktail_df=pickle.load(open('cocktail_df.pkl','rb'))

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(cocktail_df['ingredients'])
arr = X.toarray()

similarity_table = pd.DataFrame(cosine_similarity(arr), columns=cocktail_df['drink'], index=cocktail_df['drink'])
for column in similarity_table.columns:
    similarity_table[column] = np.where(similarity_table[column] >= 1, 0, similarity_table[column])
similar_cocktail= similarity_table.idxmax()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data=request.json['data']
    print(data)
    # print(list(data.values()))
    ## print(np.array(list(data.values())).reshape(1,-1))
    output=similar_cocktail[data['drink']]
    return jsonify(output)


if __name__=="__main__":
    app.run(debug=True)


