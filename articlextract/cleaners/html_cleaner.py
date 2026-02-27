import re

TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")

def clean_html(text: str | None) -> str | None:
    """
    Remove HTML tags and normalize whitespace.
    """

    if not text or not isinstance(text, str):
        return None

    try:
        # Remove tags
        text = TAG_RE.sub(" ", text)

        # Normalize whitespace
        text = SPACE_RE.sub(" ", text)

        return text.strip() or None

    except Exception:
        return None