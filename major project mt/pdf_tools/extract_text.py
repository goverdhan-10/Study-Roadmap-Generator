# pdf_tools/extract_text.py

from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:

    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    all_text = []
    for page in doc:
        all_text.append(page.get_text("text"))
    doc.close()
    return "\n".join(all_text)


def extract_text_from_txt(txt_path: str) -> str:
    """
    Simple TXT reader.
    """
    txt_path = Path(txt_path)
    if not txt_path.exists():
        raise FileNotFoundError(f"TXT file not found: {txt_path}")
    return txt_path.read_text(encoding="utf-8", errors="ignore")


def load_text_auto(path: str) -> str:
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        return extract_text_from_pdf(str(path))
    elif path.suffix.lower() in {".txt", ".md"}:
        return extract_text_from_txt(str(path))
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")
