from ollama import AsyncClient


class DeepSeekChat:
    def __init__(self, model: str = "deepseek-r1:1.5b"):
        self.client = AsyncClient()
        self.model = model
        self.messages_history = []

    async def chat(self, prompt: str) -> str:
        """Возвращает полный ответ"""
        self._add_message('user', prompt)

        response = await self.client.chat(
            model=self.model,
            messages=self.messages_history
        )

        full_response = response['message']['content']
        self._add_message('assistant', full_response)
        return full_response

    def reset_history(self):
        self.messages_history = []

    def _add_message(self, role: str, content: str):
        self.messages_history.append({
            'role': role,
            'content': content
        })

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.client.close()