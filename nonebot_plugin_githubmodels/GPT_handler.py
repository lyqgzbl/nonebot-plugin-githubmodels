from openai import AsyncOpenAI

class GPTHandler:
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
        self.client = AsyncOpenAI(base_url=endpoint, api_key=api_key)
        self.model_name = model_name
        self.max_context_length = max_context_length
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p

    async def get_response(self, messages: list) -> str:
        response = await self.client.chat.completions.create(
            messages=messages,
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
        )
        return response.choices[0].message.content