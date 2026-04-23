# pdf_tools/batch_process.py
import json
from pathlib import Path
from typing import Optional

from .extract_text import load_text_auto
from .parse_result import analyze_text
from .db_store import init_db, save_analysis


def process_single_file(file_path: str, outputs_dir: str = "outputs") -> str:

    Path(outputs_dir).mkdir(parents=True, exist_ok=True)

    text = load_text_auto(file_path)
    analysis = analyze_text(text)

    # save JSON
    output_name = Path(file_path).stem + "_analysis.json"
    output_path = Path(outputs_dir) / output_name
    output_path.write_text(json.dumps(analysis, indent=2), encoding="utf-8")

    # save to DB
    init_db()
    save_analysis(file_path, analysis)

    return str(output_path)


def process_all_samples(
    samples_dir: str = "samples", outputs_dir: str = "outputs"
) -> None:
    samples_path = Path(samples_dir)
    if not samples_path.exists():
        print(f"[WARN] samples folder not found: {samples_dir}")
        return

    files = list(samples_path.glob("*.pdf")) + list(samples_path.glob("*.txt"))
    if not files:
        print(f"[INFO] No PDF/TXT files found in {samples_dir}")
        return

    print(f"[INFO] Found {len(files)} files in {samples_dir}")
    for f in files:
        print(f"[INFO] Processing {f.name} ...")
        out = process_single_file(str(f), outputs_dir=outputs_dir)
        print(f"   -> Saved analysis: {out}")
