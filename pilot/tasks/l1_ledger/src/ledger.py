'''Ledger parsing and analytics.'''
import json
from datetime import date
from typing import Iterable


def parse_line(line: str) -> dict:
    raise NotImplementedError


def balances(lines: Iterable[str]) -> dict[str, int]:
    raise NotImplementedError


def top_accounts(bal: dict[str, int], n: int) -> list[tuple[str, int]]:
    raise NotImplementedError


def summarize(path: str) -> dict:
    raise NotImplementedError
