import asyncio
from DeepSeekOllamaTest import DeepSeekChat
from chat_gui import ChatGUI

async def main():
    async with DeepSeekChat() as chat_client:
        gui = ChatGUI(chat_client)
        gui.run()

if __name__ == "__main__":
    asyncio.run(main())