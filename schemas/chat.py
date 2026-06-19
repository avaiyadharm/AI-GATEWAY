from pydantic import BaseModel, Field
from typing import Literal, Optional


class ChatRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="The question or message to send to the model"
    )
    provider: Literal["groq", "openrouter"] = Field(
        ...,
        description="Which provider to use: 'groq' or 'openrouter'"
    )
    model: str = Field(
        ...,
        description="The model name (e.g. 'llama3-8b-8192' for Groq)"
    )
    max_tokens: int = Field(
        default=4096,
        ge=1,
        le=8192,
        description="Maximum tokens in the response"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature: 0 = deterministic, 2 = very random"
    )
    system_prompt: Optional[str] = Field(
        default=None,
        description="Optional system prompt to set the assistant's behaviour"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the capital of France?",
                "provider": "groq",
                "model": "llama-3.1-8b-instant",
                "max_tokens": 500,
                "temperature": 0.7
            }
        }


class ChatResponse(BaseModel):
    response: str = Field(description="The model's reply")
    provider: str = Field(description="Which provider was used")
    model: str = Field(description="Which model was used")
    input_tokens: Optional[int] = Field(default=None)
    output_tokens: Optional[int] = Field(default=None)