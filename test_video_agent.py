import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from agents.video_agent import VideoAgent

# Load env
load_dotenv()

def test_video_agent():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found")
        return

    agent = VideoAgent(api_key)
    
    # Test video: "Me at the zoo" (very short)
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    print(f"Testing with URL: {url}")
    
    try:
        # Test ID extraction
        video_id = agent.extract_video_id(url)
        print(f"✅ Extracted Video ID: {video_id}")
        
        # Test Transcript
        print("Fetching transcript...")
        transcript = agent.get_transcript(video_id)
        print(f"✅ Transcript (first 50 chars): {transcript[:50]}...")
        
        # Test Summarization
        print("Summarizing...")
        summary = agent.summarize(url)
        print(f"✅ Summary:\n{summary}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_video_agent()
