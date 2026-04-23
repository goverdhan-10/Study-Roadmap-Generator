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

    clean = clean_text(text)

    # Predict subject using trained ML model
    predicted_subject, _ = predict_subject(clean)

    # Load CSV subject-topic map
    subject_topic_map = load_subject_topic_map(csv_path)

    # Match subject properly
    matched_subject = None
    for sub in subject_topic_map.keys():
        if normalize(sub) == normalize(predicted_subject):
            matched_subject = sub
            break

    if not matched_subject:
        matched_subject = predicted_subject.lower()

    # Detect prerequisites (strict word match)
    prerequisites: List[str] = []
    clean_tokens = set(clean.split())

    if matched_subject in subject_topic_map:
        for topic in subject_topic_map[matched_subject]:
            topic_norm = normalize(topic)

            for word in clean_tokens:
                if normalize(word) == topic_norm:
                    prerequisites.append(topic)
                    break

    # Remove duplicates
    prerequisites = list(dict.fromkeys(prerequisites))

    # Generate roadmap from Wikipedia
    study_roadmap = generate_intelligent_roadmap(prerequisites)

    return {
        "predicted_subject": matched_subject,
        "prerequisites": prerequisites,
        "study_roadmap": study_roadmap
    }
