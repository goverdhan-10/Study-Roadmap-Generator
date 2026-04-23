from pathlib import Path
import json
from collections import Counter
from typing import List, Tuple, Optional

MODEL_PATH = Path("models") / "tfidf_model_manual.json"
MODEL_PATH.parent.mkdir(exist_ok=True)

def save_manual_tfidf_model(idf: dict, default_idf: float, N_docs: int):
    data = {"idf": idf, "default_idf": default_idf, "N_docs": N_docs}
    with MODEL_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f)

def load_manual_tfidf_model() -> Optional[dict]:
    if not MODEL_PATH.exists():
        return None
    with MODEL_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def compute_term_scores(tokens: List[str], top_k: int = 25) -> List[Tuple[str, float]]:
    if not tokens:
        return []
    tf = Counter(tokens)
    model = load_manual_tfidf_model()
    if model is None:
        
        items = [(t, float(c)) for t, c in tf.items()]
        items.sort(key=lambda x: x[1], reverse=True)
        return items[:top_k]
    idf = model.get("idf", {})
    default_idf = model.get("default_idf", 1.0)
    scores = []
    for term, freq in tf.items():
        score = freq * idf.get(term, default_idf)
        scores.append((term, float(score)))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]
