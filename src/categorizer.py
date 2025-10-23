# src/categorizer.py
import openai
import random
from src.config import OPENAI_API_KEY, MODEL, CATEGORIES

openai.api_key = OPENAI_API_KEY
cache = {}

# simple keyword fallback rules (K-beauty friendly)
KEYWORD_MAP = {
    "foam": "Cleanser",
    "cleansing": "Cleanser",
    "cleanser": "Cleanser",
    "wash": "Cleanser",
    "toner": "Toner",
    "essence": "Essence",
    "serum": "Serum",
    "ampoule": "Serum",
    "cream": "Moisturizer",
    "sun": "Sunscreen",
    "spf": "Sunscreen",
    "mask": "Mask",
    "pack": "Mask",
    "eye": "Eye Care"
}

def keyword_fallback(name, desc):
    text = (name + " " + desc).lower()
    for word, cat in KEYWORD_MAP.items():
        if word in text:
            return cat
    return None

def make_prompt(name, desc):

    prompt = (
        "You are a skincare product classifier. "
        "Choose ONE best matching category from this list:\n"
        f"{', '.join(CATEGORIES)}.\n\n"
        "Return only the category name (no sentences).\n\n"
        f"Now classify this:\nProduct: {name}\nDescription: {desc}\nCategory:"
    )
    return prompt

def categorize_product(name, desc):
    key = (name + desc).lower()
    if key in cache:
        return cache[key]

    # keyword fallback first
    fallback = keyword_fallback(name, desc)
    if fallback:
        result = (fallback, 0.9)
        cache[key] = result
        print(f"[keyword match] {name} → {fallback}")
        return result

    prompt = make_prompt(name, desc)
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=20,
        )
        raw = response["choices"][0]["message"]["content"].strip()
        print(f"[model raw] {name}: {raw}")

        # exact or substring match
        chosen = None
        for cat in CATEGORIES:
            if cat.lower() in raw.lower():
                chosen = cat
                break
        if not chosen:
            chosen = fallback or "Other"

        conf = 0.9 if chosen != "Other" else 0.5

    except Exception as e:
        print("API error:", e)
        chosen = fallback or "Other"
        conf = 0.5

    result = (chosen, round(conf, 2))
    cache[key] = result
    print(f"[final] {name} → {chosen} ({conf})")
    return result
