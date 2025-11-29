import requests
import time

url = "http://localhost:8507"
print(f"Checking {url}...")

for i in range(10):
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("App is running!")
            break
    except requests.exceptions.ConnectionError:
        print("Connection refused, retrying...")
        time.sleep(2)
else:
    print("Failed to connect after 10 attempts.")
