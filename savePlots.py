import nltk
import pandas as pd
from nltk import FreqDist
from nltk.corpus import stopwords
from numpy import array2string
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt

merged_data = pd.read_excel(r'dataset\Patient_Records_Training_Mappe_Merged.xlsx')
df = pd.DataFrame(merged_data[merged_data["source"] == "textual"], columns=['text'])
for text in df.iterrows():
    tokenizer = nltk.RegexpTokenizer(r"[a-zA-Z]{3,}")
    strippedText = array2string(text[1].values).replace('\\n', ' ')
    word_tokens = tokenizer.tokenize(strippedText)
    stop_words = set(stopwords.words("english"))
    filtered_sentence = []
    for w in word_tokens:
        if w.lower() not in stop_words:
            filtered_sentence.append(w)
    fig = plt.figure(figsize=(10, 4))
    plt.gcf().subplots_adjust(bottom=0.15)
    fdist = FreqDist(filtered_sentence)
    fdist.plot(30, cumulative=False, linewidth=3)
    plt.show()
    fig.savefig('tokenizeFilteredPunctuationRegex.png', bbox_inches = "tight")