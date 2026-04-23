import pickle
from pathlib import Path
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

import re
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def clean_token(word: str):
    """
    Simple normalization:
    - lowercase
    - remove non-letters
    - length >= 3
    - lemmatize
    """
    word = word.lower().strip()
    if len(word) < 3:
        return None
    if not re.match(r"[a-zA-Z]+", word):
        return None
    return lemmatizer.lemmatize(word)


def train_model_from_multiple_pdfs(all_term_scores):
    
    cleaned_terms = []
    labels = []

    for term_scores in all_term_scores:
        if len(term_scores) < 5:
            
            continue

        
        term_scores = sorted(term_scores, key=lambda x: x[1], reverse=True)
        cut = max(1, len(term_scores) // 3)  # top 1/3 ko important

        for idx, (term, score) in enumerate(term_scores):
            tok = clean_token(term)
            from pathlib import Path
from collections import Counter
import csv
import math

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from pdf_tools.extract_text import load_text_auto


# ---- basic NLP setup (manual, no sklearn) ----

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

EN_STOPWORDS = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def preprocess(text: str):
    """
    Simple manual preprocessing:
    - lowercase
    - tokenization (regex)
    - alphabetic tokens only
    - stopword removal
    - lemmatization
    """
    import re

    text = text.lower()
    tokens = re.findall(r"[a-z]+", text)
    cleaned = []
    for tok in tokens:
        if tok in EN_STOPWORDS:
            continue
        if len(tok) <= 2:
            continue
        lemma = lemmatizer.lemmatize(tok)
        cleaned.append(lemma)
    return cleaned


def main():
    train_dir = Path("training_pdfs")

    if not train_dir.exists():
        print("[ERROR] 'training_pdfs' folder missing.")
        return

    files = list(train_dir.glob("*.pdf"))
    if not files:
        print("[ERROR] No PDFs found inside training_pdfs.")
        return

    print(f"[INFO] Found {len(files)} training PDFs.")

    # sab docs ke tokens store karenge
    all_doc_tokens = []
    doc_names = []

    # document frequency ke liye
    df_counter = Counter()

    for f in files:
        print(f"[INFO] Reading: {f.name}")
        try:
            text = load_text_auto(str(f))
            tokens = preprocess(text)
            if not tokens:
                print(f"[WARN] No tokens after preprocessing for {f.name}, skipping.")
                continue

            all_doc_tokens.append(tokens)
            doc_names.append(f.name)

            unique_terms = set(tokens)
            for term in unique_terms:
                df_counter[term] += 1

        except Exception as e:
            print(f"[WARN] Skipped {f.name} due to error: {e}")

    if not all_doc_tokens:
        print("[ERROR] No usable documents; cannot train.")
        return

    N_docs = len(all_doc_tokens)
    print(f"[INFO] Training on {N_docs} documents.")

    # IDF compute (manual)
    idf = {}
    for term, df in df_counter.items():
        # log((N+1)/(df+1)) + 1 to avoid div by zero
        idf_val = math.log((N_docs + 1) / (df + 1)) + 1.0
        idf[term] = idf_val

    default_idf = math.log(N_docs + 1)  # for unseen terms

    # training_terms.csv me per-term tf-idf + label (1=advanced,0=basic) daalenge
    rows_for_csv = []

    for doc_name, tokens in zip(doc_names, all_doc_tokens):
        tf = Counter(tokens)

        # tf-idf scores
        term_scores = []
        for term, freq in tf.items():
            score = freq * idf.get(term, default_idf)
            term_scores.append((term, score))

        # importance ke hisaab se sort
        term_scores.sort(key=lambda x: x[1], reverse=True)

        if not term_scores:
            continue

        cut = max(1, len(term_scores) // 3)  # top 1/3 as advanced

        for idx, (term, score) in enumerate(term_scores):
            label = 1 if idx < cut else 0
            rows_for_csv.append((doc_name, term, float(score), label))

    # save training_terms.csv (INPUT + LABEL) for you to see
    out_csv = Path("training_terms.csv")
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["pdf_file", "term", "tfidf_score", "label"])
        writer.writerows(rows_for_csv)
    print(f"[INFO] Saved training terms to {out_csv}")

    # model ko json me save karte hain (IDF + default)
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    model_path = model_dir / "tfidf_model_manual.json"

    import json

    model_data = {
        "N_docs": N_docs,
        "idf": idf,
        "default_idf": default_idf,
    }

    with model_path.open("w", encoding="utf-8") as f:
        json.dump(model_data, f)

    print(f" Trained manual TF-IDF model saved to {model_path}")


if _name_ == "_main_":
    main()