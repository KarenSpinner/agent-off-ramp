'''Strict unified-diff application.'''
import re


class PatchError(ValueError):
    pass


def apply_unified(text: str, patch: str) -> str:
    '''Apply ``patch`` to ``text``; see task.md.'''
    raise NotImplementedError
