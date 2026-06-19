from openai import AsyncOpenAI
from fastapi import HTTPException
import os

def build_messages(query: str, history: list, system_prompt: str = None):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": query})
    return messages

async def call_openrouter(query: str, model: str, max_tokens: int,
temperature: float, system_prompt: str = None, history: list = []) -> dict:
    client = AsyncOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "LLM Gateway"
        }
    )
    messages = build_messages(query, history, system_prompt)
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return {
            "response": response.choices[0].message.content,
            "provider": "openrouter",
            "model": model,
            "input_tokens": response.usage.prompt_tokens if response.usage else None,
            "output_tokens": response.usage.completion_tokens if response.usage else None
        }
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg:
            raise HTTPException(status_code=401, detail="Invalid OpenRouter API key.")
        elif "429" in error_msg:
            raise HTTPException(status_code=429, detail="OpenRouter rate limit hit.")
        elif "404" in error_msg:
            raise HTTPException(status_code=404, detail=f"Model '{model}' not found on OpenRouter.")
        else:
            raise HTTPException(status_code=500, detail=f"OpenRouter error: {error_msg}")

async def call_openrouter_stream(query: str, model: str, max_tokens: int,
temperature: float, system_prompt: str = None, history: list = []):
    client = AsyncOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "LLM Gateway"
        }
    )
    messages = build_messages(query, history, system_prompt)
    try:
        stream = await client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )
        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                words = content.split(' ')
                for i, word in enumerate(words):
                    if i < len(words) - 1:
                        yield word + ' '
                    else:
                        yield word
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg:
            raise HTTPException(status_code=401, detail="Invalid OpenRouter API key.")
        elif "429" in error_msg:
            raise HTTPException(status_code=429, detail="OpenRouter rate limit hit.")
        elif "404" in error_msg:
            raise HTTPException(status_code=404, detail=f"Model '{model}' not found on OpenRouter.")
        else:
            raise HTTPException(status_code=500, detail=f"OpenRouter error: {error_msg}")