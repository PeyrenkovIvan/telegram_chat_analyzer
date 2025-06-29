from telethon.sync import TelegramClient
from telethon.tl.types import User
from datetime import datetime, timedelta
import json
import os

# Загрузка конфигурации
with open("config.json", "r") as f:
    config = json.load(f)

api_id = config["api_id"]
api_hash = config["api_hash"]
phone = config["phone"]

# Инициализация клиента
client = TelegramClient("session", api_id, api_hash)

# Авторизация
async def start_client():
    await client.start(phone)
    print("✅ Успешная авторизация")

# Получение личных чатов (без ботов, каналов, групп)
async def fetch_chats():
    me = await client.get_me()
    my_id = me.id

    dialogs = await client.get_dialogs(limit=50)
    chat_list = []

    for dialog in dialogs:
        entity = dialog.entity
        if isinstance(entity, User) and not entity.bot and entity.id != my_id:
            chat_list.append(entity)

    return chat_list

# Сбор сообщений за последние N дней
async def fetch_messages(chat, days=30):
    since = datetime.now() - timedelta(days=days)
    messages = []

    async for msg in client.iter_messages(chat.id, offset_date=since, reverse=True):
        messages.append({
            "text": msg.message or "",
            "timestamp": msg.date.isoformat(),
            "sender": "manager" if msg.out else "client"
        })

    return messages

# Сохранение всех переписок в JSON
async def save_chat_history():
    os.makedirs("data", exist_ok=True)
    chats = await fetch_chats()

    for chat in chats:
        messages = await fetch_messages(chat)
        filename = f"data/chat_{chat.id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "chat_id": chat.id,
                "title": getattr(chat, 'first_name', 'NoTitle'),
                "messages": messages
            }, f, ensure_ascii=False, indent=2)

    print("💾 История сохранена в папку /data")
