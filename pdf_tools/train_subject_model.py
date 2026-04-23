import pandas as pd
import time
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
import joblib

# ==============================
# TRAIN NAIVE BAYES MODEL
# ==============================

CSV_PATH = "major-project-data-word (1).csv"

print(" Loading dataset...")

df = pd.read_csv(CSV_PATH, on_bad_lines="skip", engine="python")
df = df.dropna()

df["Subject"] = df["Subject"].astype(str)
df["Topic"] = df["Topic"].astype(str)

X = []
y = []

for subject, group in df.groupby("Subject"):
    text = " ".join(group["Topic"].tolist())
    X.append(text)
    y.append(subject)

print(" Training Naive Bayes model...")

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])

model.fit(X, y)

# save model
joblib.dump(model, "models/subject_model.pkl")

print(" Naive Bayes model trained and saved!")

# ==============================
# TEST + TIME MEASURE
# ==============================

from pdf_tools.extract_text import load_text_auto
from pdf_tools.parse_result import analyze_text

file_path = r"train_uploads/yourfile.pdf"   # 👉 CHANGE THIS

if not Path(file_path).exists():
    print(" File not found! Fix path.")
    exit()

print("\n STARTING FULL ANALYSIS...\n")

# ⏱ START TIME
start_time = time.time()

# FULL PIPELINE
text = load_text_auto(file_path)
result = analyze_text(text, CSV_PATH)

# ⏱ END TIME
end_time = time.time()
total_time = round(end_time - start_time, 4)

# ==============================
# OUTPUT
# ==============================

print("====================================")
print(" File:", file_path)
print(" Predicted Subject:", result["predicted_subject"])

print("\n Prerequisites:")
for p in result["prerequisites"]:
    print("-", p)

print(f"\n TOTAL PROCESSING TIME: {total_time} seconds")
print("====================================")