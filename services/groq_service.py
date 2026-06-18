from groq import AsyncGroq
from fastapi import HTTPException
import os


async def call_groq(
    query: str,
    model: str,
    max_tokens: int,
    temperature: float,
    system_prompt: str = None
) -> dict:
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

    # Build the messages list
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
            "provider": "groq",
            "model": model,
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens
        }

    except Exception as e:
        error_msg = str(e)

        # Give the user a meaningful error, not a raw SDK traceback
        if "401" in error_msg or "invalid_api_key" in error_msg.lower():
            raise HTTPException(status_code=401, detail="Invalid Groq API key.")
        elif "429" in error_msg:
            raise HTTPException(status_code=429, detail="Groq rate limit hit. Try again shortly.")
        elif "model_not_found" in error_msg.lower() or "404" in error_msg:
            raise HTTPException(status_code=404, detail=f"Model '{model}' not found on Groq.")
        else:
            raise HTTPException(status_code=500, detail=f"Groq error: {error_msg}")