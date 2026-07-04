"""
decorators.py
--------------
Yahan ek decorator hai jo har action (add, update, delete)
ko automatically log kar deta hai - bina har function mein
manually likhe.
"""
from datetime import datetime
from functools import wraps


def log_action(func):
    """
    Ye decorator kisi bhi function ke upar laga do,
    wo function chalne se pehle aur baad log message print karega
    aur log.txt file mein bhi likh dega.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] Action: {func.__name__} | Args: {args[1:]}"

        # Terminal pe dikhana
        print(f"LOG -> {log_message}")

        # log.txt file mein likhna (append mode)
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(log_message + "\n")

        return result
    return wrapper