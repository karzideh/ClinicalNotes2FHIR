import pandas as pd
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.ensemble import RandomForestClassifier
import pickle

merged_data = pd.read_excel(r'dataset\Patient_Records_Training_Mappe_Merged.xlsx')
df = pd.DataFrame(merged_data[merged_data["source"] == "textual"], columns=['text'])
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

for disease in df:
    disease[1]['filtered'] = disease[1]['text'].apply(
        lambda x: " ".join(
            [stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in stop_words]).lower())
    vectorizer = TfidfVectorizer(min_df=3, stop_words="english", sublinear_tf=True, ngram_range=(1, 2))
    final_features = vectorizer.fit_transform(disease[1]['filtered']).toarray()
    X = disease[1]['filtered']
    Y = disease[1]['judgment']
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25)
    pipeline = Pipeline([('vect', vectorizer),
                         ('chi', SelectKBest(chi2, k=1200)),
                         ('clf', RandomForestClassifier())])
    model = pipeline.fit(X_train, y_train)
    with open('RandomForest.pickle', 'wb') as f:
        pickle.dump(model, f)
    ytest = np.array(y_test)
    print("")
    print("Classification results for disease: "+disease[0])
    print("")
    print(classification_report(ytest, model.predict(X_test)))
    print(confusion_matrix(ytest, model.predict(X_test)))