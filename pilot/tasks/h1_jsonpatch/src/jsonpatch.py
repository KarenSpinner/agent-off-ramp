'''RFC 6902 JSON Patch over plain Python dicts and lists.'''
import copy
import re


class PatchError(ValueError):
    pass


def apply_patch(doc, patch: list[dict]):
    '''Apply ``patch`` to ``doc`` and return the new document; see task.md.'''
    raise NotImplementedError
