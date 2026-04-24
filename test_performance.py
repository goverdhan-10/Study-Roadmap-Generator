import time
from pathlib import Path

from pdf_tools.extract_text import load_text_auto
from pdf_tools.parse_result import analyze_text

CSV = "major-project-data-word (1).csv"


def run_full_pipeline(file_path):

    print("\n==========================================")
    print(" FULL PIPELINE PERFORMANCE TEST")
    print("==========================================")
    print(f" File: {file_path}")

    if not Path(file_path).exists():
        print(" File not found! Fix path.")
        return

    # ⏱ TOTAL START
    total_start = time.time()

    # -------- STEP 1: TEXT EXTRACTION --------
    t1 = time.time()
    text = load_text_auto(file_path)
    t2 = time.time()

    # -------- STEP 2: FULL ANALYSIS --------
    t3 = time.time()
    result = analyze_text(text, CSV)
    t4 = time.time()

    # ⏱ TOTAL END
    total_end = time.time()

    # -------- TIMES --------
    extraction_time = round(t2 - t1, 4)
    analysis_time = round(t4 - t3, 4)
    total_time = round(total_end - total_start, 4)

    # -------- OUTPUT --------
    print("\n TIMING BREAKDOWN")
    print("------------------------------------------")
    print(f"Text Extraction Time  : {extraction_time} sec")
    print(f"Analysis Time         : {analysis_time} sec")
    print(f"TOTAL PROCESS TIME    : {total_time} sec")

    print("\n FINAL OUTPUT")
    print("------------------------------------------")
    print(f"Predicted Subject     : {result['predicted_subject']}")

    print("\nPrerequisites:")
    if result["prerequisites"]:
        for p in result["prerequisites"]:
            print(" -", p)
    else:
        print("None detected")

    print("\nDefinitions Generated:")
    for item in result["study_roadmap"]:
        print(f"\n🔹 {item['topic']}:")
        print(item["definition"])

    print("\n==========================================\n")


if __name__ == "__main__":
    
    # Check the uploads folder
    upload_dir = Path("uploads")
    
    # Grab all PDFs in the folder
    available_pdfs = list(upload_dir.glob("*.pdf"))
    
    if available_pdfs:
        # Automatically use the first PDF it finds
        file_path = str(available_pdfs[0])
        run_full_pipeline(file_path)
    else:
        print("❌ No PDFs found in the 'uploads' folder! Please place at least one PDF there.")