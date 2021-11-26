import nltk
import pandas as pd
from nltk import FreqDist, WordNetLemmatizer
from nltk.corpus import stopwords
from numpy import array2string
from sklearn.feature_extraction.text import CountVectorizer

text_data = pd.read_excel(r'dataset\Patient_Records_Training_Mappe.xlsx',
                          sheet_name='doc')
CountVec = CountVectorizer(ngram_range=(1, 1),
                           stop_words='english')

df = pd.DataFrame(text_data, columns=['text'])
for text in df.iterrows():
    tokenizer = nltk.RegexpTokenizer(r"[a-zA-Z]{3,}")
    strippedText = array2string(text[1].values).replace('\\n', ' ')
    word_tokens = tokenizer.tokenize(strippedText)

    stop_words = set(stopwords.words("english"))
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    lem = WordNetLemmatizer()

    lemmatized_words = []
    for w in filtered_sentence:
        lemmatized_words.append(lem.lemmatize(w, "v"))

    print("Filtered Sentence:", filtered_sentence)
    print("Lemmatized Sentence:", lemmatized_words)