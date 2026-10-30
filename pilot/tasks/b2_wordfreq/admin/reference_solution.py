import re
from collections import Counter

STOPWORDS = {
    "the", "and", "to", "a", "of", "it", "she", "i", "you", "in", "was", "that", "as",
    "her", "with", "at", "on", "all", "this", "for", "had", "but", "be", "not", "they",
    "so", "very", "what", "t", "s",
}


def top_words(path: str, n: int = 10) -> list[tuple[str, int]]:
    with open(path, encoding="utf-8") as f:
        words = [w for w in re.split(r"[^a-z]+", f.read().lower()) if w and w not in STOPWORDS]
    counts = Counter(words)
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:n]
