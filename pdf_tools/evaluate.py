# pdf_tools/evaluate.py
import csv
from typing import List, Set

def _to_set(items: List[str]) -> Set[str]:
    return set(x.strip().lower() for x in items if x.strip())

def evaluate(predicted: List[str], actual: List[str]):
    pred_set = _to_set(predicted)
    act_set = _to_set(actual)

    tp = len(pred_set & act_set)
    fp = len(pred_set - act_set)
    fn = len(act_set - pred_set)

    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0

    return precision, recall, f1


def load_ground_truth(path: str = "ground_truth.csv"):
    truth = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            truth[row["file_name"]] = [
                x.strip() for x in row["actual_prerequisites"].split(",")
            ]
    return truth

