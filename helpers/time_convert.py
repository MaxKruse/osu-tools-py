from datetime import timedelta

from click import FloatRange


def timedelta_to_ms(td: timedelta) -> float:
    res = td.microseconds / 1000.0 + td.seconds * 1000.0 + td.days * 24 * 60 * 60 * 1000.0
    return res