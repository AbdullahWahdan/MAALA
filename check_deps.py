import sys

required_imports = [
    "streamlit",
    "langchain",
    "langchain_community",
    "langchain_core",
    "langchain_groq",
    "langchain_huggingface",
    "langchain_chroma",
    "chromadb",
    "sentence_transformers",
    "pypdf",
    "arxiv",
    "wikipedia",
    "duckduckgo_search",
    "dotenv"
]

print(f"Python executable: {sys.executable}")
print("Checking imports...")

missing = []
for module in required_imports:
    try:
        __import__(module)
        print(f"✅ {module}")
    except ImportError as e:
        print(f"❌ {module}: {e}")
        missing.append(module)

if missing:
    print(f"\nMissing packages: {', '.join(missing)}")
    sys.exit(1)
else:
    print("\nAll packages installed.")
    sys.exit(0)
