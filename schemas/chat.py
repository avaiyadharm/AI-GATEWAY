from pydantic import BaseModel, Field
from typing import Literal, Optional, List

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1)
    provider: Literal["groq", "openrouter"]
    model: str
    max_tokens: int = Field(default=4096, ge=1, le=8192)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    system_prompt: Optional[str] = None
    history: Optional[List[Message]] = Field(
        default=[],
        description="Previous messages in the conversation"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is recursion?",
                "provider": "groq",
                "model": "llama-3.1-8b-instant",
                "max_tokens": 4096,
                "temperature": 0.7,
                "history": [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi! How can I help?"}
                ]
            }
        }

class ChatResponse(BaseModel):
    response: str
    provider: str
    model: str
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None