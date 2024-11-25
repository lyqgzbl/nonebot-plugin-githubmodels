from typing import Optional
from pydantic import BaseModel, Field

class Config(BaseModel):
    github_token: Optional[str] = None
    ai_model_name: str = "gpt-4o-mini"
    max_context_length: int = Field(20, gt=0)
    ai_reply_image: bool = False
