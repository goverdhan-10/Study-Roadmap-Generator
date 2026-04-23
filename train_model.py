import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path

# ---------------- CONFIG ----------------

CSV_PATH = "major-project-data-word (1).csv"

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "subject_classifier.pkl"


def train_model():

    print("Loading dataset...")

    df = pd.read_csv(
        CSV_PATH,
        engine="python",
        on_bad_lines="skip"
    )

    df = df.dropna()

    df["Subject"] = df["Subject"].astype(str)
    df["Topic"] = df["Topic"].astype(str)

    # remove accidental pdf rows
    df = df[~df["Subject"].str.contains(".pdf", case=False)]

    X = []
    y = []

    for subject, group in df.groupby("Subject"):

        topics = group["Topic"].tolist()

        text = " ".join(topics)

        X.append(text)
        y.append(subject)

    print("\nTraining samples\n")

    for a, b in zip(X, y):
        print(b, "->", a[:80], "...")

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1,2)
        )),
        ("clf", MultinomialNB())
    ])

    pipeline.fit(X, y)

    joblib.dump(pipeline, MODEL_PATH)

    print("\nModel saved at:", MODEL_PATH)


if __name__ == "__main__":
    train_model()