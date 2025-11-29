import langchain
print(f"LangChain version: {langchain.__version__}")
print(f"LangChain file: {langchain.__file__}")
try:
    import langchain.chains
    print("✅ langchain.chains imported")
    print(dir(langchain.chains))
except ImportError as e:
    print(f"❌ langchain.chains failed to import: {e}")
