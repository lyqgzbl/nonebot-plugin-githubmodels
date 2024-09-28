from typing import Optional
from pydantic import BaseModel, field_validator

class Config(BaseModel):
    github_token: Optional[str] = None
    ai_model_name: str = "gpt-4o-mini"
    MAX_CONTEXT_LENGTH: int = 20

    @field_validator("MAX_CONTEXT_LENGTH")
    @classmethod
    def check_max_context_length(cls, v: int) -> int:
        if v > 0:
            return v
        raise ValueError("MAX_CONTEXT_LENGTH must be greater than 0")
