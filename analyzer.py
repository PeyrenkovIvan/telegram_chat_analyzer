import os
import json
from ai_module import (
    detect_broken_promise,
    detect_negative_sentiment,
    detect_low_initiative,
)
from datetime import datetime
import pandas as pd


def analyze_chat(chat_data):
    messages = chat_data["messages"]

    result = {
        "chat_id": chat_data["chat_id"],
        "title": chat_data["title"],
        "broken_promise": detect_broken_promise(messages),
        "negative": detect_negative_sentiment(messages),
        "low_initiative": detect_low_initiative(messages),
        "total_messages": len(messages),
        "avg_reply_time_minutes": calculate_avg_reply_time(messages),
    }

    return result


def calculate_avg_reply_time(messages):
    """
    Подсчёт среднего времени ответа менеджера (в минутах)
    """
    reply_times = []
    last_client_msg_time = None

    for msg in messages:
        ts = datetime.fromisoformat(msg["timestamp"])

        if msg["sender"] == "client":
            last_client_msg_time = ts

        elif msg["sender"] == "manager" and last_client_msg_time:
            delta = (ts - last_client_msg_time).total_seconds() / 60
            if 0 < delta < 600:  # разумный предел — 10 часов
                reply_times.append(delta)
            last_client_msg_time = None

    if not reply_times:
        return None

    return round(sum(reply_times) / len(reply_times), 2)


def run_analysis():
    results = []
    data_dir = "data"

    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            with open(os.path.join(data_dir, filename), "r", encoding="utf-8") as f:
                chat_data = json.load(f)
                result = analyze_chat(chat_data)
                results.append(result)

    # Вывод в консоль
    for r in results:
        print(
            f"{r['title']} | Обещание НЕ выполнено: {r['broken_promise']} | "
            f"Негатив: {r['negative']} | Пассивность: {r['low_initiative']} | "
            f"Средний ответ: {r['avg_reply_time_minutes']} мин"
        )

    # Сохранение в CSV
    df = pd.DataFrame(results)
    df.to_csv("chat_analysis_report.csv", index=False)
    print("📁 Отчёт сохранён в chat_analysis_report.csv")
