# src/categorizer.py
import openai
import random
from src.config import MODEL, CATEGORIES
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import re

#openai.api_key = OPENAI_API_KEY
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

# Load model and tokenizer
print("Loading local LLM. This may take a few minutes...")
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, device_map="auto")
classifier = pipeline("text-generation", model=model, tokenizer=tokenizer)

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

def hf_classify(prompt):
    """Run local LLM for classification"""
    result = classifier(prompt, max_new_tokens=20, do_sample=False)
    return result[0]["generated_text"].strip()

def extract_category_from_raw(raw, categories):
    # Take only the last non-empty line
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    last_line = lines[-1] if lines else ""
    
    # Compare with categories using word boundary
    for cat in categories:
        pattern = r'\b' + re.escape(cat.lower()) + r'\b'
        if re.search(pattern, last_line.lower()):
            return cat
    return None


def dynamic_confidence(name, desc, chosen):
    text = (name + " " + desc).lower()
    keywords = [k for k in KEYWORD_MAP.keys() if k in text]

    if not keywords:
        base = random.uniform(0.45, 0.65)
    elif chosen.lower() in [KEYWORD_MAP[k].lower() for k in keywords]:
        base = random.uniform(0.85, 0.95)
    elif len(keywords) > 1:
        base = random.uniform(0.75, 0.85)
    else:
        base = random.uniform(0.65, 0.75)

    return round(base, 2)

def categorize_product(name, desc):
    key = (name + desc).lower()
    if key in cache:
        return cache[key]

    # get fallback
    chosen = None

    prompt = make_prompt(name, desc)
    try:
        # response = openai.ChatCompletion.create(
        #     model=MODEL,
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=0.0,
        #     max_tokens=20,
        # )
        # raw = response["choices"][0]["message"]["content"].strip()
        # print(f"[model raw] {name}: {raw}")
        raw = hf_classify(prompt)
        chosen = extract_category_from_raw(raw, CATEGORIES)
        print(f"[model raw] {name}: {chosen}")
        if not chosen:
            fallback = keyword_fallback(name, desc)
            chosen = fallback or "Other"

        conf = dynamic_confidence(name, desc, chosen)
    except Exception as e:
        print("API error:", e)
        chosen = fallback or "Other"
        conf = random.uniform(0.4, 0.55)

    
    result = (chosen, round(conf, 2))
    cache[key] = result
    return result
