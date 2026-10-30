import os


def normalize(path: str) -> str:
    return os.path.realpath(os.path.abspath(path))
