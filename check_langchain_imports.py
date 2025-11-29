try:
    from langchain.chains import create_history_aware_retriever
    print("✅ create_history_aware_retriever found in langchain.chains")
except ImportError as e:
    print(f"❌ create_history_aware_retriever NOT found in langchain.chains: {e}")

try:
    from langchain.chains import create_retrieval_chain
    print("✅ create_retrieval_chain found in langchain.chains")
except ImportError:
    print("❌ create_retrieval_chain NOT found in langchain.chains")

try:
    from langchain.chains.combine_documents import create_stuff_documents_chain
    print("✅ create_stuff_documents_chain found in langchain.chains.combine_documents")
except ImportError:
    print("❌ create_stuff_documents_chain NOT found in langchain.chains.combine_documents")
