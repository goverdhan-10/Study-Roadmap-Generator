from pathlib import Path
import csv
import nltk

from pdf_tools.extract_text import load_text_auto
from pdf_tools.parse_result import _tfidf_keywords
from pdf_tools.train_model import train_model_from_multiple_pdfs


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

    # --- COMPLEX WORDS INPUT FROM USER ---
    complex_words_file = Path("complex_words.txt")
    complex_words = set()
    if complex_words_file.exists():
        for line in complex_words_file.read_text(encoding="utf-8").splitlines():
            w = line.strip().lower()
            if w:
                complex_words.add(w)
        print(f"[INFO] Loaded {len(complex_words)} user-defined complex words from complex_words.txt")
    else:
        print("[INFO] No complex_words.txt found. Using only TF-IDF based labels.")

    all_term_scores = []
    rows_for_csv = []

    for f in files:
        print(f"[INFO] Processing: {f.name}")
        try:
            text = load_text_auto(str(f))
            sentences = nltk.sent_tokenize(text)
            term_scores = _tfidf_keywords(sentences, top_k=40)

            if term_scores:
                sorted_terms = sorted(term_scores, key=lambda x: x[1], reverse=True)
                cut = max(1, len(sorted_terms) // 3)

                for idx, (term, score) in enumerate(sorted_terms):
                    term_lower = term.lower()

                    # default label based on TF-IDF rank
                    label = 1 if idx < cut else 0

                    # OVERRIDE: if user marked this as complex word
                    if term_lower in complex_words:
                        label = 1

                    rows_for_csv.append(
                        (f.name, term, float(score), label)
                    )

            all_term_scores.append(term_scores)
        except Exception as e:
            print(f"[WARN] Skipped {f.name} due to error: {e}")

    # --- SAVE TRAINING TERMS + LABELS FOR USER ---
    if rows_for_csv:
        with open("training_terms.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["pdf_file", "term", "tfidf_score", "label"])
            writer.writerows(rows_for_csv)
        print("📄 Saved training terms + labels to training_terms.csv")

    if not all_term_scores:
        print("[ERROR] No term scores collected. Cannot train model.")
        return

    print("[INFO] Training ML model (Logistic Regression)...")
    train_model_from_multiple_pdfs(all_term_scores)

    print(" Model trained and saved to models/difficulty_model.pkl")


if __name__ == "__main__":
    main()
