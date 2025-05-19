import asyncio
from typing import AsyncGenerator
from ollama import AsyncClient


class DeepSeekChat:
    def __init__(self, model: str = "deepseek-r1:1.5b"):
        self.client = AsyncClient()
        self.model = model
        self.messages_history = []

    async def chat_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """Асинхронный генератор для потокового ответа"""
        self._add_message('user', prompt)

        response = await self.client.chat(
            model=self.model,
            messages=self.messages_history,
            stream=True
        )

        full_response = []
        async for chunk in response:
            content = chunk['message']['content']
            full_response.append(content)
            yield content

        self._add_message('assistant', ''.join(full_response))

    async def chat(self, prompt: str) -> str:
        """Синхронный интерфейс для получения полного ответа"""
        response = []
        async for chunk in self.chat_stream(prompt):
            response.append(chunk)
        return ''.join(response)

    def reset_history(self):
        """Сброс истории разговора"""
        self.messages_history = []

    def _add_message(self, role: str, content: str):
        """Внутренний метод для добавления сообщений в историю"""
        self.messages_history.append({
            'role': role,
            'content': content
        })

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.client.close()