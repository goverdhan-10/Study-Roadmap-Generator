import csv
from collections import defaultdict
from pathlib import Path

def load_subject_topic_map(csv_path):
    mapping = defaultdict(list)
    with open(csv_path, encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                sub = row[0].strip().lower()
                topic = row[1].strip().lower()
                mapping[sub].append(topic)
    return dict(mapping)
