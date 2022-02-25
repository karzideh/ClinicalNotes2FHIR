import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.ensemble import RandomForestClassifier

import pickle
import warnings

warnings.filterwarnings('ignore')

# annotation data from i2b2 obesity dataset
training_data = pd.read_csv(
    r'dataset\training_data.csv')
test_data = pd.read_csv(
    r'dataset\test_data.csv')

# creating data_frames from the data
# here can be decided, if the intuitive or textual task should be done
df_train = pd.DataFrame(training_data[training_data["source"] == "intuitive"]).groupby("disease")
df_test = pd.DataFrame(test_data[test_data["source"] == "intuitive"]).groupby("disease")

for disease in df_train:
    for disease_test in df_test:
        if(disease[0] == disease_test[0]):
            X_train = disease[1]['fhir_info']
            y_train = disease[1]['judgment']
            X_test = disease_test[1]['fhir_info']
            y_test = disease_test[1]['judgment']
            vectorizer = TfidfVectorizer(min_df=6, stop_words="english", sublinear_tf=True, ngram_range=(1, 2))
            final_features = vectorizer.fit_transform(disease[1]['fhir_info']).toarray()
            pipeline = Pipeline([('vect', vectorizer),
                                 ('chi', SelectKBest(chi2, k=1800)),
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
