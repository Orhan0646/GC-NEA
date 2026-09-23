import requests

response = requests.post("http://127.0.0.1:5000/delete-question/1")
print(f"Status code: {response.status_code}")
print(f"Response: {response.text}")