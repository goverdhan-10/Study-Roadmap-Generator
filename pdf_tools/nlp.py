# pdf_tools/nlp.py

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from typing import List

def ensure_nltk():
    try:
        _ = stopwords.words("english")
    except LookupError:
        nltk.download("stopwords")

    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        nltk.download("wordnet")

ensure_nltk()

EN_STOPWORDS = set(stopwords.words("english"))
_LEMMATIZER = WordNetLemmatizer()


def tokenize_sentences(text: str) -> List[str]:
    return nltk.sent_tokenize(text)


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z]+", text.lower())


def preprocess_tokens(text: str) -> List[str]:
    tokens = _tokenize(text)
    out = []
    for t in tokens:
        if t in EN_STOPWORDS:
            continue
        if len(t) <= 2:
            continue
        out.append(_LEMMATIZER.lemmatize(t))
    return out
