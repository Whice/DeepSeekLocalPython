import asyncio
from DeepSeekOllamaTest import DeepSeekChat


async def main():
    async with DeepSeekChat() as chatbot:
        while True:
            user_input = input("\nВы: ")

            # Потоковый вывод
            print("Ассистент: ", end='', flush=True)
            async for chunk in chatbot.chat_stream(user_input):
                print(chunk, end='', flush=True)

            # Или получение полного ответа
            # full_response = await chatbot.chat(user_input)
            # print(f"\nАссистент: {full_response}")


if __name__ == "__main__":
    asyncio.run(main())