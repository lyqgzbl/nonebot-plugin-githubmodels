from typing import Optional
from nonebot import get_plugin_config
from pydantic import BaseModel, Field

class Config(BaseModel):
  token: Optional[str] = Field(default=None)
  model_name: Optional[str] = Field(default=“gpt-4o-mini”)
  MAX_CONTEXT_LENGTH: Optionsl[int] = Field(defalut=20)

plugin_config: Config = get_plugin_config(Config)
TOKEN = plugin_config.github_token
MODEL_NAME = plugin_config.model_name
MAX_CONTEXT_LENGTH = plugin_config.MAX_CONTEXT_LENGTH
