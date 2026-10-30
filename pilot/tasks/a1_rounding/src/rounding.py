'''Half-away-from-zero rounding utilities.'''
from decimal import Decimal


def round_half_up(x: float, ndigits: int = 0) -> float:
    '''Round ``x`` to ``ndigits`` places with ties rounding away from zero.'''
    raise NotImplementedError
