from fastapi import FastAPI
from routers import chat
from dotenv import load_dotenv
import os

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("GROQ_API_KEY is not set. Check your .env file.")
if not os.getenv("OPENROUTER_API_KEY"):
    raise RuntimeError("OPENROUTER_API_KEY is not set. Check your .env file.")

app = FastAPI(
    title="LLM Gateway API",
    description="Query multiple LLM providers through a single API",
    version="1.0.0"
)

app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "LLM Gateway is running. Visit /docs to test it."}
