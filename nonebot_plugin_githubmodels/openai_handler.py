from collections.abc import Sequence
from azure.ai.inference.aio import ChatCompletionsClient
from azure.ai.inference.models import ChatRequestMessage
from azure.core.credentials import AzureKeyCredential


class OPENAI_Handler:
    def __init__(
        self,
        api_key: str,
        endpoint: str,
        model_name: str,
        max_context_length: int,
        temperature: float,
        max_tokens: int,
        top_p: float,
    ):
        self.client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key)
        )
        self.model_name = model_name
        self.max_context_length = max_context_length
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p

    async def get_response(self, messages: Sequence[ChatRequestMessage]) -> str:
        response = await self.client.complete(
            messages=list(messages),
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("模型未返回内容")
        return content
