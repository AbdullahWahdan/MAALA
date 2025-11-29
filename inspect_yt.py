from youtube_transcript_api import YouTubeTranscriptApi
print(dir(YouTubeTranscriptApi))
try:
    print("Trying static get_transcript...")
    print(YouTubeTranscriptApi.get_transcript("jNQXAC9IVRw"))
except Exception as e:
    print(f"Static failed: {e}")

try:
    print("Trying instance fetch...")
    api = YouTubeTranscriptApi()
    print(api.fetch("jNQXAC9IVRw"))
except Exception as e:
    print(f"Instance failed: {e}")
