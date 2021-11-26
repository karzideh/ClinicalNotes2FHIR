import pandas as pd
from numpy import array2string
from sklearn.feature_extraction.text import TfidfVectorizer

text_data = pd.read_excel(r'dataset\Patient_Records_Training_Mappe.xlsx', sheet_name='doc')

tf_idf_vec = TfidfVectorizer(use_idf=True,
                        smooth_idf=False,
                        ngram_range=(1,1),stop_words='english')

tf_idf_vec_smooth = TfidfVectorizer(use_idf=True,
                        smooth_idf=True,
                        ngram_range=(1,1),stop_words='english')

df = pd.DataFrame(text_data, columns = ['text'])
for text in df.iterrows():
    tf_idf_data = tf_idf_vec.fit_transform([array2string(text[1].values)])
    tf_idf_dataframe = pd.DataFrame(tf_idf_data.toarray(), columns=tf_idf_vec.get_feature_names())
    print("Without Smoothing:")
    print(tf_idf_dataframe)
    print("\n")

    tf_idf_data_smooth = tf_idf_vec_smooth.fit_transform([array2string(text[1].values)])
    tf_idf_dataframe_smooth = pd.DataFrame(tf_idf_data_smooth.toarray(), columns=tf_idf_vec_smooth.get_feature_names())
    print("With Smoothing:")
    print(tf_idf_dataframe_smooth)
    print("\n")