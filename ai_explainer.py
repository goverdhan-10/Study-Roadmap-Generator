from transformers import pipeline

# model load (ek baar hi load hoga)
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

def explain_concept(term):
    prompt = f"""
    Explain the concept '{term}' in Computer Science.

    Give:
    - definition
    - one example
    - 3-4 lines

    Do not leave answer blank.
    """

    result = generator(
        prompt,
        max_length=120,
        min_length=40,
        do_sample=True,
        temperature=0.7
    )

    return result[0]['generated_text'].strip()