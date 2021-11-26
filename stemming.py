import nltk
import pandas as pd
from nltk.corpus import stopwords
from numpy import array2string
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer

diseases_data = pd.read_excel(r'dataset\Patient_Records_Training_Mappe.xlsx', sheet_name='diseases')
text_data = pd.read_excel(r'dataset\Patient_Records_Training_Mappe.xlsx', sheet_name='doc')
CountVec = CountVectorizer(ngram_range=(1,1),
                           stop_words='english')

df = pd.DataFrame(text_data, columns = ['text'])

for text in df.iterrows():
    tokenizer = nltk.RegexpTokenizer(r"[a-zA-Z]{3,}")
    strippedText = array2string(text[1].values).replace('\\n', ' ')
    word_tokens = tokenizer.tokenize(strippedText)

    stop_words = set(stopwords.words("english"))
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    ps = PorterStemmer()
    stemmed_words = []
    for w in filtered_sentence:
        stemmed_words.append(ps.stem(w))

    print("Unfiltered Sentence:", word_tokens)
    print("Filtered Sentence:", filtered_sentence)
    print("Stemmed Sentence:", stemmed_words)