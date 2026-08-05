import logging
import re
import time
from typing import List

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("GenkitChatbot")

def clean_text(text: str) -> str:
    """Removes extra whitespace and cleans special characters."""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def format_timestamp(ts: float = None) -> str:
    """Returns ISO format timestamp."""
    if ts is None:
        ts = time.time()
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))

def truncate_tokens(tokens: List[str], max_len: int) -> List[str]:
    """Truncates list of tokens to maximum length."""
    return tokens[:max_len]
