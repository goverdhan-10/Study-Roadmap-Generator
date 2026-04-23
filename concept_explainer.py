# pdf_tools/concept_explainer.py

from typing import Dict
import re


def cs_contextize(term: str, wiki_text: str) -> Dict:
    """
    Convert Wikipedia content into Computer Science explanation
    for ANY prerequisite.
    """

    term_title = term.title()

    wiki_text = re.sub(r"\s+", " ", wiki_text).strip()

    definition = wiki_text.split(".")[0] + "."

    return {
        "title": term_title,
        "definition": f"In Computer Science, {definition}",

        "types": [
            f"Different types of {term_title} used in Computer Science",
            f"Advanced variations of {term_title}"
        ],

        "examples": [
            f"Use of {term_title} in algorithms",
            f"Real-world CS applications of {term_title}"
        ],

        "topics": [
            f"Introduction to {term_title}",
            f"Properties and characteristics",
            f"Operations on {term_title}",
            f"Applications in algorithms",
            f"Time and space complexity"
        ]
    }
