import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

print("Initializing Embeddings...")
try:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    print("✅ Embeddings initialized")
except Exception as e:
    print(f"❌ Embeddings initialization failed: {e}")
    exit(1)

print("Testing Embedding Generation...")
try:
    vec = embeddings.embed_query("Hello world")
    print(f"✅ Embedding generated (len={len(vec)})")
except Exception as e:
    print(f"❌ Embedding generation failed: {e}")
    exit(1)

print("Testing Chroma VectorStore...")
try:
    docs = [
        Document(page_content="The topic of this document is Machine Learning.", metadata={"source": "test.pdf"}),
        Document(page_content="Support Vector Machines are a type of supervised learning algorithm.", metadata={"source": "test.pdf"})
    ]
    
    vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings, collection_name="test_collection")
    print("✅ VectorStore created")
    
    retriever = vectorstore.as_retriever()
    results = retriever.invoke("What is the topic?")
    
    print(f"Retrieved {len(results)} documents")
    for doc in results:
        print(f"- {doc.page_content}")
        
    if len(results) > 0:
        print("✅ Retrieval successful")
    else:
        print("❌ Retrieval returned no results")
        
except Exception as e:
    print(f"❌ VectorStore test failed: {e}")
