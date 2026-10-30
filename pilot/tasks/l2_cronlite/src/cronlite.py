'''A three-field cron subset.'''
from datetime import datetime, timedelta


def next_run(spec: str, after: datetime) -> datetime:
    '''Return the first matching time strictly after ``after``; see task.md.'''
    raise NotImplementedError
