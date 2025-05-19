import argparse
from ollama import chat
from ollama import ChatResponse

messages_history = []  # Храним всю историю сообщений

while True:
    user_message = input("Вы: ")
    
    # Добавляем сообщение пользователя в историю
    messages_history.append({
        'role': 'user',
        'content': user_message,
    })

    model = "deepseek-r1:1.5b"
    full_response = ""
    
    # Отправляем всю историю модели
    response: ChatResponse = chat(
        model=model,
        messages=messages_history,
        stream=True
    )

    print("Ассистент: ", end='', flush=True)
    for chunk in response:
        chunk_content = chunk['message']['content']
        full_response += chunk_content
        print(chunk_content, end='', flush=True)
    
    # Добавляем ответ ассистента в историю
    messages_history.append({
        'role': 'assistant',
        'content': full_response,
    })
    
    print("\n")
