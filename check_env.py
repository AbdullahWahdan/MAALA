import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GROQ_API_KEY")
if key:
    print("GROQ_API_KEY is found.")
else:
    print("GROQ_API_KEY is MISSING.")
