import re
from typing import List, Dict, Any
import wikipedia
import streamlit as st

from pdf_tools.match_keywords import load_subject_topic_map
from pdf_tools.prerequisite_graph import build_graph
from pdf_tools.predict_subject import predict_subject
from pdf_tools.learning_order import generate_learning_order


# ---------------- CLEAN TEXT ---------------- #

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize(s: str) -> str:
    return re.sub(r"[^a-z]", "", s.lower())


# ---------------- FIXED DEFINITIONS (PRIORITY OVERRIDE) ---------------- #

CS_FIXED_DEFINITIONS = {
    "agent": "An agent is an entity in artificial intelligence that perceives its environment and takes actions to achieve specific goals.",
    "environment": "In artificial intelligence, the environment is everything external to an agent that it interacts with to perform tasks.",
    "actions": "Actions are the operations or decisions taken by an agent in response to its environment in a computational system.",
    "variables": "Variables are named storage locations in programming used to hold and manipulate data values.",
    "domains": "A domain refers to a specific area of knowledge or application in which a problem or system operates.",
    "constraints": "Constraints are conditions or rules that must be satisfied when solving a computational problem.",
    "resolution": "Resolution is a rule of inference used in logic and artificial intelligence for automated reasoning.",
    "planning": "Planning in AI involves generating a sequence of actions to achieve a defined goal from an initial state.",
    "regression": "Regression is a statistical and machine learning technique used to model relationships between variables.",
    "robotics": "Robotics is a field of computer science and engineering focused on designing and controlling intelligent machines.",
    "sensors": "Sensors are devices that collect data from the environment and provide input to computational systems or agents.",
    "inference": "Inference is the process of deriving logical conclusions from data or knowledge in artificial intelligence.",
    "reasoning": "Reasoning is the ability of a system to process information and draw conclusions based on logic.",
    "learning": "Learning in AI refers to the process by which systems improve performance based on data and experience.",
    "classification": "Classification is a machine learning task that involves assigning data into predefined categories.",
    "clustering": "Clustering is an unsupervised learning technique used to group similar data points together."
}


# ---------------- WIKIPEDIA FUNCTION ---------------- #

# ---------------- WIKIPEDIA FUNCTION (UPGRADED) ---------------- #

@st.cache_data(show_spinner=False)
def get_wiki_definition(topic):
    topic_key = topic.lower().strip()

    # PRIORITY: fixed definitions first
    if topic_key in CS_FIXED_DEFINITIONS:
        return {
            "definition": CS_FIXED_DEFINITIONS[topic_key],
            "url": None
        }

    try:
        results = wikipedia.search(topic + " computer science")
        if not results:
            return None

        # Fetch page to get the exact URL
        page = wikipedia.page(results[0], auto_suggest=False)
        summary = wikipedia.summary(results[0], sentences=2).replace("\n", " ").strip()

        return {
            "definition": summary,
            "url": page.url
        }
    except:
        return None
# ---------------- MAIN FUNCTION ---------------- #

def analyze_text(text: str, csv_path: str) -> Dict[str, Any]:

    # -------- CLEAN TEXT --------
    clean = clean_text(text)

    # -------- SUBJECT PREDICTION --------
    predicted_subject = predict_subject(clean)

    # -------- LOAD SUBJECT TOPICS --------
    subject_topic_map = load_subject_topic_map(csv_path)

    matched_subject = None

    for sub in subject_topic_map.keys():
        if normalize(sub) == normalize(predicted_subject):
            matched_subject = sub
            break

    if not matched_subject:
        matched_subject = predicted_subject

    # -------- DETECT PREREQUISITES --------
   # -------- DETECT PREREQUISITES --------
    prerequisites: List[str] = []
    clean_tokens = set(clean.split())

    if matched_subject in subject_topic_map:
        for topic in subject_topic_map[matched_subject]:
            topic_norm = normalize(topic)
            for word in clean_tokens:
                if normalize(word) == topic_norm:
                    prerequisites.append(topic)
                    break

    prerequisites = list(dict.fromkeys(prerequisites))

    # 🔥 THE FALLBACK LOGIC 🔥
    if len(prerequisites) == 0:
        if matched_subject in subject_topic_map:
            # Take top 3 topics if no exact words matched
            prerequisites = subject_topic_map[matched_subject][:3]
        else:
            prerequisites = ["Data Structures", "Algorithms", "Computer Networks"]

    # -------- GENERATE ROADMAP (WIKI + FIXED) --------
    study_roadmap = []

    for topic in prerequisites:
        wiki_data = get_wiki_definition(topic)

        # Fallback string if Wiki fails
        if not wiki_data:
            study_roadmap.append({
                "topic": topic,
                "definition": f"{topic.title()} is a fundamental concept in Computer Science.",
                "url": None
            })
            continue

        study_roadmap.append({
            "topic": topic,
            "definition": wiki_data["definition"],
            "url": wiki_data["url"]
        })

    # -------- GENERATE GRAPH --------
    graph_file = build_graph(prerequisites, matched_subject)

    # -------- SMART LEARNING ORDER --------
    learning_order, clean_relations = generate_learning_order(prerequisites)

    return {
        "predicted_subject": matched_subject,
        "prerequisites": prerequisites,
        "study_roadmap": study_roadmap,
        "learning_order": learning_order,
        "relations": clean_relations,
        "graph": graph_file
    }