import os
<<<<<<< HEAD
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-yourkey")
=======
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
>>>>>>> 13ece96 (Remove hardcoded OpenAI API key)
MODEL = "gpt-3.5-turbo"
CATEGORIES = ["Cleanser", "Toner", "Essence", "Serum", "Moisturizer",
              "Mask", "Sunscreen", "Makeup Remover", "Eye Care", "Other"]
