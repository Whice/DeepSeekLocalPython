# chat_gui.py
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import asyncio
from queue import Queue


class ChatGUI:
    def __init__(self, chat_client):
        self.chat_client = chat_client
        self.root = tk.Tk()
        self.root.title("DeepSeek Chat")
        self.root.geometry("800x600")

        self.message_queue = Queue()
        self.setup_ui()
        self.setup_async_loop()

    def setup_async_loop(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.run_async_loop, daemon=True)
        self.thread.start()

    def run_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.output_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            state='disabled',
            font=('Arial', 12)
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X)

        self.input_entry = ttk.Entry(input_frame, font=('Arial', 12))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_entry.bind("<Return>", lambda event: self.send_message())

        send_button = ttk.Button(
            input_frame,
            text="Отправить",
            command=self.send_message
        )
        send_button.pack(side=tk.RIGHT)

        self.root.after(100, self.check_queue)

    def send_message(self):
        user_input = self.input_entry.get()
        if not user_input:
            return

        self.input_entry.delete(0, tk.END)
        self.display_message("Вы", user_input)

        asyncio.run_coroutine_threadsafe(
            self.process_message(user_input),
            self.loop
        )

    async def process_message(self, user_input):
        # Получаем полный ответ вместо потока
        full_response = await self.chat_client.chat(user_input)
        self.message_queue.put(('full', full_response))

    def display_message(self, sender, message):
        self.output_area.config(state='normal')
        self.output_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.output_area.config(state='disabled')
        self.output_area.see(tk.END)

    def check_queue(self):
        while not self.message_queue.empty():
            msg_type, content = self.message_queue.get()
            if msg_type == 'full':
                self.display_message("Ассистент", content)
        self.root.after(100, self.check_queue)

    def run(self):
        self.root.mainloop()
        self.loop.call_soon_threadsafe(self.loop.stop)