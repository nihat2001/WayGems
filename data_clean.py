import re

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing URLs, HTML tags, emails, special characters,
    and normalizing whitespaces for NLP and LLM processing.
    """
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[^\w\s\.,!?]", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\S+@\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    
    text = text.lower().strip()
    return text