import re
from typing import List
import unicodedata

class Preprocessor:
    def clean_text(self, text: str) -> str:
        # Normalize and clean text
        text = unicodedata.normalize("NFKC", text)
        text = text.lower()
        text = re.sub(r"\s+", " ", text)  # Remove extra whitespace
        text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
        return text.strip()

    def chunk_text(self, text: str, chunk_size: int) -> List[str]:
        # Split text into chunks of specified size
        words = text.split()
        return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
