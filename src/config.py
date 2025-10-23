import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
MODEL = "gpt-3.5-turbo"
CATEGORIES = ["Cleanser", "Toner", "Essence", "Serum", "Moisturizer",
              "Mask", "Sunscreen", "Makeup Remover", "Eye Care", "Other"]
