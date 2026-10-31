import os

from src.wordfreq import top_words

CORPUS = os.path.join(os.path.dirname(__file__), "..", "corpus", "alice.txt")


def test_top_word():
    assert top_words(CORPUS, 1) == [("said", 462)]


def test_top_five():
    assert top_words(CORPUS, 5) == [
        ("said", 462), ("alice", 398), ("little", 128), ("one", 104), ("like", 85),
    ]


def test_n_limits():
    assert len(top_words(CORPUS, 10)) == 10
    assert len(top_words(CORPUS, 0)) == 0
