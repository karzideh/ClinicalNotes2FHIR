import pandas as pd
from numpy import array2string
from sklearn.feature_extraction.text import CountVectorizer

diseases_data = pd.read_excel(r'dataset\Patient_Records_Training_Mappe.xlsx', sheet_name='diseases')
text_data = pd.read_excel(r'dataset\Patient_Records_Training_Mappe.xlsx', sheet_name='doc')
CountVec = CountVectorizer(ngram_range=(1,1),
                           stop_words='english')

df = pd.DataFrame(text_data, columns = ['text'])
for text in df.iterrows():
    Count_data = CountVec.fit_transform([array2string(text[1].values)])
    cv_dataframe = pd.DataFrame(Count_data.toarray(), columns=CountVec.get_feature_names())
    print(cv_dataframe)