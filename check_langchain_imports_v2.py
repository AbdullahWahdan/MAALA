try:
    from langchain.chains.history_aware_retriever import create_history_aware_retriever
    print("✅ create_history_aware_retriever found in langchain.chains.history_aware_retriever")
except ImportError as e:
    print(f"❌ create_history_aware_retriever NOT found: {e}")

try:
    from langchain.chains.retrieval import create_retrieval_chain
    print("✅ create_retrieval_chain found in langchain.chains.retrieval")
except ImportError as e:
    print(f"❌ create_retrieval_chain NOT found: {e}")

try:
    from langchain.chains.combine_documents import create_stuff_documents_chain
    print("✅ create_stuff_documents_chain found in langchain.chains.combine_documents")
except ImportError as e:
    print(f"❌ create_stuff_documents_chain NOT found: {e}")
