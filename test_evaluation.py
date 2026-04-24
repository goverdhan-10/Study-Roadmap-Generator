# pdf_tools/test_evaluation.py
from pdf_tools.evaluate import evaluate, load_ground_truth

predicted_prereqs = ["tcp", "ip", "dns", "osi model"]

ground_truth = load_ground_truth("ground_truth.csv")

file_name = "cn_notes.pdf"
actual_prereqs = ground_truth.get(file_name, [])

precision, recall, f1 = evaluate(predicted_prereqs, actual_prereqs)

print("Evaluation for:", file_name)
print("Precision :", round(precision * 100, 2), "%")
print("Recall    :", round(recall * 100, 2), "%")
print("F1 Score  :", round(f1 * 100, 2), "%")
