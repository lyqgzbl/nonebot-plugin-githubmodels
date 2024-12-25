class ContextManager:
    def __init__(self, max_context_length: int):
        self.max_context_length = max_context_length
        self.shared_context = []

    def add_message(self, role: str, content: str):
        if self.max_context_length > 0:
            self.shared_context.append({"role": role, "content": content})
            if len(self.shared_context) > self.max_context_length:
                self.shared_context = self.shared_context[-self.max_context_length:]

    def get_context(self):
        return self.shared_context.copy() if self.max_context_length > 0 else []

    def reset_context(self):
        self.shared_context = []