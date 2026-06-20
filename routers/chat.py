from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from schemas.chat import ChatRequest, ChatResponse
from services.groq_service import call_groq, call_groq_stream
from services.openrouter_service import call_openrouter, call_openrouter_stream
import logging

router = APIRouter(prefix="/api", tags=["Chat"])
logger = logging.getLogger(__name__)


# ── Provider factory ──────────────────────────────────────────────────────────
def get_provider_func(provider: str):
    """Return the correct service function based on provider name."""
    providers = {
        "groq": call_groq,
        "openrouter": call_openrouter
    }
    func = providers.get(provider.lower())
    if not func:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown provider '{provider}'. Choose from: {list(providers.keys())}"
        )
    return func


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse, summary="Send a query to an LLM")
async def chat(request: ChatRequest):
    """
    Send a query to any supported LLM provider and model.

    - **provider**: `groq` or `openrouter`
    - **model**: model name for the chosen provider
    - **query**: your message
    """
    logger.info(f"Request: provider={request.provider}, model={request.model}")

    provider_func = get_provider_func(request.provider)

    result = await provider_func(
        query=request.query,
        model=request.model,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        system_prompt=request.system_prompt,
        history=request.history or []
    )

    logger.info(f"Response tokens: in={result.get('input_tokens')}, out={result.get('output_tokens')}")

    return ChatResponse(**result)


@router.post("/chat/stream", summary="Stream a response from an LLM")
async def chat_stream(request: ChatRequest):
    """Stream tokens from any supported LLM provider."""
    async def generate():
        try:
            if request.provider == "groq":
                async for token in call_groq_stream(
                    query=request.query,
                    model=request.model,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                    system_prompt=request.system_prompt,
                    history=request.history or []
                ):
                    yield token
            elif request.provider == "openrouter":
                async for token in call_openrouter_stream(
                    query=request.query,
                    model=request.model,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                    system_prompt=request.system_prompt,
                    history=request.history or []
                ):
                    yield token
        except Exception as e:
            yield f"\n\n⚠ **Error from Provider:** {str(e)}"

    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    }
    return StreamingResponse(generate(), media_type="text/event-stream", headers=headers)


@router.get("/models", summary="List available models per provider")
async def list_models():
    """Returns a static list of well-known models for each provider."""
    return {
        "groq": [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "qwen-qwen3-32b",
        ],
        "openrouter": [
            "openai/gpt-oss-120b:free",
            "openai/gpt-oss-20b:free",
            "openrouter/free"
        ]
    }

@router.get("/openrouter-models", summary="Fetch live free models from OpenRouter")
async def get_openrouter_models():
    import httpx, os
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"}
        )
        data = response.json()
        free_models = [
            m["id"] for m in data.get("data", [])
            if ":free" in m["id"]
        ]
        return {"models": free_models}