from pydantic import BaseModel, Field

class Config(BaseModel):
    github_token: str | None = None
    max_context_length: int = Field(20)
    ai_reply_image: bool = False
    ai_model_name: str = "openai/gpt-4.1-mini"
    ai_temperature: float = Field(1.0)
    ai_top_p: float = Field(1.0)
