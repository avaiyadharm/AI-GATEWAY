import requests
import json

payload = {
    "query": "What is my name?",
    "provider": "groq",
    "model": "llama-3.1-8b-instant",
    "history": [
        {"role": "user", "content": "My name is Alice."},
        {"role": "assistant", "content": "Hello Alice! How can I help you today?"}
    ]
}

res = requests.post("http://127.0.0.1:8000/api/chat", json=payload)
print("Status:", res.status_code)
print("Response:", res.json())
