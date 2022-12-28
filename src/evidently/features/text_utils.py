import string
import nltk

from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer

from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))
lem = WordNetLemmatizer()


def get_frequencies(s: str, lemmatize=True):
    word_tokens = s.split()
    res = Counter()
    for w in word_tokens:
        word = w.lower()
        if lemmatize:
            word_l = lem.lemmatize(word)
        else: word_l = word
        if word not in stop_words and word_l not in stop_words and word not in string.punctuation:
            res[word_l] += 1
    return res
