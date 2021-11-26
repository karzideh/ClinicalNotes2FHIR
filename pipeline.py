import pandas as pd
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.ensemble import RandomForestClassifier
import pickle
import warnings
import ctakes_parser as parser

warnings.filterwarnings('ignore')
training_data = pd.read_excel(
    r'dataset\Patient_Records_Training_Mappe_Merged.xlsx')

test_data = pd.read_excel(
    r'dataset\Patient_Records_Test_Mappe_Merged.xlsx')

df = parser.ctakes_parser.parse_file(file_path='dataset\Patient_Records_Test_Mappe_Merged.xlsx')

# creating data_frames from the data
# here can be decided, if the intuitive or textual task should be done
df_train = pd.DataFrame(training_data[training_data["source"] == "textual"]).groupby("disease")
df_test = pd.DataFrame(test_data[test_data["source"] == "textual"]).groupby("disease")
stop_words = set(stopwords.words("english"))

stemmer = PorterStemmer()

for disease in df_train:
    for disease_test in df_test:
        if(disease[0] == disease_test[0]):
            disease[1]['filtered'] = disease[1]['text'].apply(
                lambda x: " ".join(
                    [stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in stop_words]).lower())

            disease_test[1]['filtered'] = disease_test[1]['text'].apply(
                lambda x: " ".join(
                    [stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in stop_words]).lower())

            vectorizer = TfidfVectorizer(min_df=3, stop_words="english", sublinear_tf=True, ngram_range=(1, 2))
            final_features = vectorizer.fit_transform(disease[1]['filtered']).toarray()
            X_train = disease[1]['filtered']
            y_train = disease[1]['judgment']
            X_test = disease_test[1]['filtered']
            y_test = disease_test[1]['judgment']
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