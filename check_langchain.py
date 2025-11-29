try:
    from langchain.chains import create_history_aware_retriever
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
    import langchain
    print(f"Langchain version: {langchain.__version__}")
    print(f"Langchain file: {langchain.__file__}")
