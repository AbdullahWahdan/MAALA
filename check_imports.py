try:
    import langchain_classic
    print("langchain_classic found")
except ImportError:
    print("langchain_classic MISSING")

try:
    import sentence_transformers
    print("sentence_transformers found")
except ImportError:
    print("sentence_transformers MISSING")

try:
    from langchain_huggingface import HuggingFaceEmbeddings
    print("langchain_huggingface found")
except ImportError:
    print("langchain_huggingface MISSING")

try:
    from langchain_chroma import Chroma
    print("langchain_chroma found")
except ImportError:
    print("langchain_chroma MISSING")
