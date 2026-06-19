from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# ── CORS — allow the frontend (any origin) to call the API ────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(chat.router)

# ── Serve the frontend folder at /static (static files) ───────────────────────
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    return {"message": "LLM Gateway is running. Visit /docs for API docs or /ui for the chat UI."}

@app.get("/ui")
async def serve_ui():
    return FileResponse("frontend/llm-gateway-ui.html")

