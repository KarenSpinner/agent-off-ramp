'''Word frequency over a text corpus.'''
import re
from collections import Counter

STOPWORDS = {
    "the", "and", "to", "a", "of", "it", "she", "i", "you", "in", "was", "that", "as",
    "her", "with", "at", "on", "all", "this", "for", "had", "but", "be", "not", "they",
    "so", "very", "what", "t", "s",
}


def top_words(path: str, n: int = 10) -> list[tuple[str, int]]:
    '''Return the ``n`` most common non-stopword words in the file at ``path``.'''
    raise NotImplementedError
