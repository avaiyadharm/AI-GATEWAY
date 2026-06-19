import requests
import json

payload = {
    "query": "What did I just ask?",
    "provider": "groq",
    "model": "llama-3.1-8b-instant",
    "history": [
        {"role": "user", "content": "I have two dogs, a golden retriever named Max and a poodle named Bella."},
        {"role": "assistant", "content": "That's wonderful! Golden Retrievers and Poodles are both great breeds. How can I help you with Max and Bella today?"}
    ]
}

# we'll just test the sync endpoint because it uses the exact same build_messages
res = requests.post("http://127.0.0.1:8000/api/chat", json=payload)
print(res.json())
