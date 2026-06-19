from openai import AsyncOpenAI
from fastapi import HTTPException
import os


async def call_openrouter(
    query: str,
    model: str,
    max_tokens: int,
    temperature: float,
    system_prompt: str = None
) -> dict:
    client = AsyncOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost:8000",  # required by OpenRouter
            "X-Title": "LLM Gateway"
        }
    )

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": query})

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
                                 temperature: float, system_prompt: str = None):
    client = AsyncOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "LLM Gateway"
        }
    )
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": query})

    stream = await client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True
    )
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content