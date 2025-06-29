NEGATIVE_WORDS = [
    "плохо", "ужас", "недоволен", "чому мовчите", "не отвечает", "долго", "жах", "негатив", "дуже довго"
    ]

def detect_broken_promise(messages):
    """
    Ищет сообщения менеджера с обещанием и проверяет,
    было ли выполнено (ответ в течение 6 часов)
    """
    from datetime import datetime

    for i, msg in enumerate(messages):
        if msg["sender"] != "manager":
            continue

        if any(word in msg["text"].lower() for word in ["скину", "прорахую", "посчитаю", "отправлю", "напишу", "до вечера"]):
            promise_time = datetime.fromisoformat(msg["timestamp"])

            for followup in messages[i+1:]:
                if followup["sender"] == "manager":
                    reply_time = datetime.fromisoformat(followup["timestamp"])
                    if (reply_time - promise_time).total_seconds() <= 21600:
                        return False  # выполнено
            return True  # обещание есть, но не выполнено

    return False  # обещания нет

def detect_negative_sentiment(messages):
    """
    Ищет негативные слова в сообщениях клиента
    """
    for msg in messages:
        if msg["sender"] != "client":
            continue

        if any(word in msg["text"].lower() for word in NEGATIVE_WORDS):
            return True

    return False

def detect_low_initiative(messages):
    """
    Проверяет, был ли менеджер достаточно активен
    """
    manager_msgs = [m for m in messages if m["sender"] == "manager"]
    if len(manager_msgs) < 3:
        return True

    help_words = ["чем могу помочь", "подскажите", "готов помочь", "уточните", "дайте знать"]
    if not any(any(w in m["text"].lower() for w in help_words) for m in manager_msgs):
        return True

    return False
