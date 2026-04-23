from pathlib import Path
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    p = Path(pdf_path)
    if not p.exists():
        raise FileNotFoundError(p)
    doc = fitz.open(str(p))
    text = []
    for page in doc:
        text.append(page.get_text("text"))
    doc.close()
    return "\n".join(text)

def extract_text_from_txt(txt_path: str) -> str:
    return Path(txt_path).read_text(encoding="utf-8", errors="ignore")

def load_text_auto(path: str) -> str:
    p = Path(path)
    if p.suffix.lower() == ".pdf":
        return extract_text_from_pdf(str(p))
    elif p.suffix.lower() in [".txt", ".md"]:
        return extract_text_from_txt(str(p))
    else:
        raise ValueError("Unsupported file type")
