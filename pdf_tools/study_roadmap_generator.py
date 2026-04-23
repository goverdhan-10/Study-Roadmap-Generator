# pdf_tools/parse_result.py

import re
from typing import List, Dict, Any
from pdf_tools.match_keywords import load_subject_topic_map
from pdf_tools.intelligent_roadmap import generate_intelligent_roadmap
from subject_model import predict_subject


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize(s: str) -> str:
    return re.sub(r"[^a-z]", "", s.lower())


def analyze_text(text: str, csv_path: str) -> Dict[str, Any]:

    # 1. Clean text
    clean = clean_text(text)

    # 2. Predict subject using ML model
    predicted_subject, _ = predict_subject(clean)

    # 3. Load subject → topics map from CSV
    subject_topic_map = load_subject_topic_map(csv_path)

    # 4. Match predicted subject with CSV subjects
    matched_subject = None
    for sub in subject_topic_map.keys():
        if normalize(sub) == normalize(predicted_subject):
            matched_subject = sub
            break

    # fallback
    if not matched_subject:
        matched_subject = predicted_subject.lower()

    # 5. Detect prerequisites (WORD LEVEL MATCH)
    prerequisites: List[str] = []
    clean_tokens = set(clean.split())

    if matched_subject in subject_topic_map:
        for topic in subject_topic_map[matched_subject]:
            topic_norm = normalize(topic)
            for word in clean_tokens:
                if normalize(word) == topic_norm:
                    prerequisites.append(topic)
                    break

    # remove duplicates
    prerequisites = list(dict.fromkeys(prerequisites))

    # 6. Intelligent roadmap from Wikipedia
    study_roadmap = generate_intelligent_roadmap(prerequisites)

    return {
        "predicted_subject": matched_subject,
        "prerequisites": prerequisites,
        "study_roadmap": study_roadmap
    }
