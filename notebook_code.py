# %% Code Cell
pip install youtube-transcript-api

# %% Code Cell
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

# %% Code Cell
def extract_video_id(url: str) -> str:


  """
  Extract the YouTube video ID from a URL.
  Raises ValueError if no 'v' parameter is found.
  """
  parsed = urlparse(url)
  qs = parse_qs(parsed.query)
  video_ids = qs.get('v')

  if not video_ids:
   raise ValueError(f"No video id found in URL: {url}")
  return video_ids[0]

if __name__ == "__main__":
  url = "https://www.youtube.com/watch?v=aO1-6X_f74M"

  video_id = extract_video_id(url)

  api = YouTubeTranscriptApi()
  fetched = api.fetch(video_id, languages=['en']) # returns a FetchedTranscript

  text = "\n".join(snippet.text for snippet in fetched)

# %% Code Cell
print(text)

# %% Code Cell
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# %% Code Cell
import requests

URL = "https://raymond-exhibitable-aggravatingly.ngrok-free.dev/generate"
headers = {"Authorization": "Bearer secret123"}
payload = {
    "prompt": text,
    "max_length": 300,
    "min length":30,
    "do sample":False
}

res = requests.post(URL, headers=headers, json=payload)
answer = res.json()["response"]

# %% Code Cell
answer[0]['summary_text']

# %% Code Cell


# %% Code Cell


