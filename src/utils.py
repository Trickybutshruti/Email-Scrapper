# src/utils.py

from datetime import datetime

def current_timestamp() -> str:
    """Returns current timestamp as string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
