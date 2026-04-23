import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path

CSV_PATH = "major-project-data-word (1).csv"
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

print("[INFO] Loading CSV...")
df = pd.read_csv(CSV_PATH)

# Group topics by subject → training text
print("[INFO] Preparing training data...")
grouped = df.groupby("Subject")["Topic"].apply(lambda x: " ".join(x)).reset_index()

X = grouped["Topic"]
y = grouped["Subject"]

print("[INFO] Training TF-IDF + Logistic Regression model...")
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1,2),
        stop_words="english"
    )),
    ("clf", LogisticRegression(
        max_iter=1000,
        solver="lbfgs",
        multi_class="auto"
    ))
])

pipeline.fit(X, y)

joblib.dump(pipeline, MODEL_DIR / "subject_classifier.pkl")

print(" MODEL TRAINED & SAVED → models/subject_classifier.pkl")
