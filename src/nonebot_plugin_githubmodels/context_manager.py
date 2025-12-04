from __future__ import annotations
from azure.ai.inference.models import (
    AssistantMessage,
    ChatRequestMessage,
    SystemMessage,
    UserMessage,
)


class ContextManager:
    def __init__(self, max_context_length: int):
        self.max_context_length = max_context_length
        self.shared_context: list[ChatRequestMessage] = []

    def add_message(self, role: str, content: str):
        if self.max_context_length <= 0:
            return

        message = self._create_message(role, content)
        if message is None:
            return

        self.shared_context.append(message)
        if len(self.shared_context) > self.max_context_length:
            self.shared_context = self.shared_context[-self.max_context_length:]

    def get_context(self) -> list[ChatRequestMessage]:
        return self.shared_context.copy() if self.max_context_length > 0 else []

    def reset_context(self):
        self.shared_context = []

    @staticmethod
    def _create_message(role: str, content: str) -> ChatRequestMessage | None:
        if role == "user":
            return UserMessage(content=content)
        if role == "assistant":
            return AssistantMessage(content=content)
        if role == "system":
            return SystemMessage(content=content)
        return None
