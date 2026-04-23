import joblib
from pathlib import Path

MODEL_PATH = Path("models/subject_classifier.pkl")

def predict_subject(text):
    if not MODEL_PATH.exists():
        return "unknown", []
    model = joblib.load(MODEL_PATH)
    probs = model.predict_proba([text])[0]
    labels = model.classes_
    return labels[probs.argmax()], probs
