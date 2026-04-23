import os
import csv
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

FOLDER = "training_pdfs"
os.makedirs(FOLDER, exist_ok=True)

styles = getSampleStyleSheet()

TOPICS = {
    "Computer Networks": [
        "router", "switch", "OSI model", "TCP", "UDP", "IP addressing", "subnetting"
    ],
    "Databases": [
        "SQL", "normalization", "primary key", "foreign key", "transaction", "indexing"
    ],
    "Artificial Intelligence": [
        "search", "heuristic", "state space", "knowledge representation", "inference"
    ],
    "Operating Systems": [
        "process", "thread", "scheduling", "deadlock", "paging", "virtual memory"
    ],
    "Data Structures": [
        "array", "linked list", "stack", "queue", "tree", "graph", "hashing"
    ],
    "Machine Learning": [
        "training data", "feature", "label", "classification", "regression", "overfitting"
    ],
    "Cloud Computing": [
        "virtualization", "IaaS", "PaaS", "SaaS", "scalability", "multi-tenancy"
    ],
    "Cyber Security": [
        "encryption", "firewall", "malware", "authentication", "intrusion detection"
    ],
    "Big Data": [
        "Hadoop", "HDFS", "MapReduce", "YARN", "distributed processing"
    ],
    "Software Engineering": [
        "SDLC", "requirements", "UML", "testing", "maintenance"
    ],
}


LABELS_FILE = "training_labels.csv"

def main():
    labels_rows = []

    topic_names = list(TOPICS.keys())
    num_topics = len(topic_names)

    for i in range(1, 1001):   # 1000 PDFs
        topic = topic_names[i % num_topics]
        terms = TOPICS[topic]

        filename = f"{topic.replace(' ', '_').lower()}_{i}.pdf"
        path = os.path.join(FOLDER, filename)

        
        text = (
            f"This is training PDF number {i} for the topic {topic}. "
            f"In {topic}, important concepts include: {', '.join(terms)}. "
            "This material describes basic definitions, advantages, disadvantages, and use cases. "
            "Students should understand these terms before moving to advanced topics."
        )

        doc = SimpleDocTemplate(path, pagesize=letter)
        story = [Paragraph(text, styles["Normal"])]
        doc.build(story)

        
        for term in terms:
            labels_rows.append((filename, term, 1))

    
    non_important = ["introduction", "example", "student", "course", "chapter", "section"]
    for i in range(1, 1001):
        filename = f"{topic_names[i % num_topics].replace(' ', '_').lower()}_{i}.pdf"
        for term in non_important:
            labels_rows.append((filename, term, 0))

    
    with open(LABELS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["pdf_file", "term", "label"])  # header
        writer.writerows(labels_rows)

    print(" 1000 PDFs created in 'training_pdfs' and labels stored in 'training_labels.csv'.")

if __name__ == "__main__":
    main()

