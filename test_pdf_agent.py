import os
import sys
from dotenv import load_dotenv

# Load env vars
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ GROQ_API_KEY not found")
    sys.exit(1)

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from agents.pdf_agent.core import PDFAgent

print("Initializing PDFAgent...")
agent = PDFAgent(api_key)

print("Processing PDF...")
target_pdf = "proposal.pdf" if os.path.exists("proposal.pdf") else "test_svm.pdf"
print(f"Using PDF: {target_pdf}")

try:
    num_chunks = agent.process_pdf(target_pdf)
    print(f"✅ Processed PDF into {num_chunks} chunks")
except Exception as e:
    print(f"❌ PDF processing failed: {e}")
    sys.exit(1)

print("Querying Agent...")
question = "Summarize this document."
print(f"Question: {question}")

try:
    response = agent.get_response(question, "test_session_1")
    print(f"Response:\n{response}")
    
    if "not enough information" in response.lower() or "i don't know" in response.lower():
        print("❌ Agent failed to answer correctly")
    else:
        print("✅ Agent answered")
except Exception as e:
    print(f"❌ Query failed: {e}")
