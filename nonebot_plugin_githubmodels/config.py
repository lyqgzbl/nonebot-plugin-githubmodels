from typing import Optional
from pydantic import BaseModel, Field

class Config(BaseModel):
    github_token: Optional[str] = None
    max_context_length: int = Field(20)
    ai_reply_image: bool = False
    ai_model_name: str = "gpt-4o-mini"
    ai_temperature: float = Field(1.0)
    ai_max_tokens: int = Field(1024)
    ai_top_p: float = Field(1.0)