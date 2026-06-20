import requests
import time
import sys
import json

payload = {
    "query": "Tell me a joke",
    "provider": "groq",
    "model": "llama-3.1-8b-instant",
    "history": []
}

start = time.time()
res = requests.post("http://127.0.0.1:8000/api/chat/stream", json=payload, stream=True)

if res.status_code != 200:
    print(f"Error: {res.status_code} {res.text}")
    sys.exit(1)

first_chunk_time = None
chunk_count = 0

for chunk in res.iter_content(chunk_size=None):
    if chunk:
        now = time.time()
        if first_chunk_time is None:
            first_chunk_time = now
            print(f"Time to first chunk: {first_chunk_time - start:.3f}s")
        chunk_count += 1
        sys.stdout.write(chunk.decode('utf-8'))
        sys.stdout.flush()

end = time.time()
print(f"\n\nTotal time: {end - start:.3f}s")
print(f"Total chunks: {chunk_count}")
if chunk_count > 1:
    print(f"Average time between chunks: {(end - first_chunk_time) / (chunk_count - 1):.3f}s")
