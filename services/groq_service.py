from groq import AsyncGroq
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

async def call_groq(query: str, model: str, max_tokens: int,
temperature: float, system_prompt: str = None, history: list = []) -> dict:
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
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
            "provider": "groq",
            "model": model,
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens
        }
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "invalid_api_key" in error_msg.lower():
            raise HTTPException(status_code=401, detail="Invalid Groq API key.")
        elif "429" in error_msg:
            raise HTTPException(status_code=429, detail="Groq rate limit hit.")
        elif "404" in error_msg or "model_not_found" in error_msg.lower() or "model_decommissioned" in error_msg.lower():
            raise HTTPException(status_code=404, detail=f"Model '{model}' not found on Groq.")
        else:
            raise HTTPException(status_code=500, detail=f"Groq error: {error_msg}")

async def call_groq_stream(query: str, model: str, max_tokens: int,
temperature: float, system_prompt: str = None, history: list = []):
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
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
            raise HTTPException(status_code=401, detail="Invalid Groq API key.")
        elif "429" in error_msg:
            raise HTTPException(status_code=429, detail="Groq rate limit hit.")
        elif "404" in error_msg or "model_not_found" in error_msg.lower() or "model_decommissioned" in error_msg.lower():
            raise HTTPException(status_code=404, detail=f"Model '{model}' not found on Groq.")
        else:
            raise HTTPException(status_code=500, detail=f"Groq error: {error_msg}")