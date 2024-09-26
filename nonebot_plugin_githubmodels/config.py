from typing import Optional
from nonebot import get_driver
from nonebot import get_plugin_config

class Config:
    def __init__(self):
        try:
            self.github_token = get_driver().config.github_token  
        except AttributeError:
            self.github_token = None
            
        try:
            self.model_name = get_driver().config.model_name
        except AttributeError:
            self.model_name = "gpt-4o-mini"
            
        try:
            self.MAX_CONTEXT_LENGTH = get_driver().config.MAX_CONTEXT_LENGTH
        except AttributeError:
            self.MAX_CONTEXT_LENGTH = 20

config = Config()  
TOKEN = config.github_token 
MODEL_NAME = config.model_name
MAX_CONTEXT_LENGTH = config.MAX_CONTEXT_LENGTH