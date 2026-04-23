from typing import List, Dict
import wikipedia
import re


# ---------------- CLEAN TEXT ---------------- #

def _clean_text(text: str) -> str:
    text = re.sub(r"\[[0-9]+\]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _get_first_paragraph(content: str) -> str:
    paragraphs = content.split("\n\n")
    for para in paragraphs:
        para = para.strip()
        if len(para) > 80:
            return _clean_text(para)[:600]
    return ""


# ---------------- WIKIPEDIA FETCH ---------------- #

def _fetch_definition(term: str) -> str:

    wikipedia.set_lang("en")

    search_variants = [
        term + " (computer science)",
        term + " (data structure)",
        term + " (algorithm)",
        term
    ]

    for variant in search_variants:
        try:
            page = wikipedia.page(variant, auto_suggest=True)
            definition = _get_first_paragraph(page.content)
            if definition:
                return definition
        except wikipedia.DisambiguationError as e:
            # try first CS related option
            for option in e.options:
                if "computer" in option.lower() or "data" in option.lower():
                    try:
                        page = wikipedia.page(option)
                        definition = _get_first_paragraph(page.content)
                        if definition:
                            return definition
                    except:
                        continue
        except:
            continue

    return None


# ---------------- MAIN FUNCTION ---------------- #

def generate_intelligent_roadmap(prerequisites: List[str]) -> List[Dict]:

    roadmap = []

    for term in prerequisites:

        definition = _fetch_definition(term)

        if not definition:
            definition = f"{term.title()} is a fundamental concept in Computer Science."

        roadmap.append({
            "topic": term.title(),
            "definition": definition,
            "types": [],
            "components": []
        })

    return roadmap