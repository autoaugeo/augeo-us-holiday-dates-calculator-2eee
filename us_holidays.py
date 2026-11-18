"""US holiday date calculator (standard library only).

Functions:
    federal_holidays(year) -> list of (name, actual date, observed date)
    easter(year)           -> Easter Sunday (anonymous Gregorian algorithm)
    easter_related(year)   -> Ash Wednesday, Palm Sunday, Good Friday
    dst_us(year)           -> (DST start, DST end) under current US rules

Command line:
    python us_holidays.py 2027
"""
import sys
from datetime import date, timedelta

MONDAY, THURSDAY, SUNDAY = 0, 3, 6


def nth_weekday(year, month, weekday, n):
    """The n-th (1-based) given weekday of a month."""
    first = date(year, month, 1)
    offset = (weekday - first.weekday()) % 7
    return first + timedelta(days=offset + 7 * (n - 1))


def last_weekday(year, month, weekday):
    """The last given weekday of a month."""
    if month == 12:
        last = date(year, 12, 31)
    else:
        last = date(year, month + 1, 1) - timedelta(days=1)
    return last - timedelta(days=(last.weekday() - weekday) % 7)


def observed(actual):
    """Federal observed rule: Saturday -> Friday, Sunday -> Monday."""
    if actual.weekday() == 5:
        return actual - timedelta(days=1)
    if actual.weekday() == 6:
        return actual + timedelta(days=1)
    return actual


def federal_holidays(year):
    """The 11 US federal holidays as (name, actual date, observed date).

    Observed dates can fall in an adjacent year (New Year's Day on a
    Saturday is observed on Dec 31 of the previous year).
    """
    fixed = [
        ("New Year's Day", date(year, 1, 1)),
        ("Juneteenth National Independence Day", date(year, 6, 19)),
        ("Independence Day", date(year, 7, 4)),
        ("Veterans Day", date(year, 11, 11)),
        ("Christmas Day", date(year, 12, 25)),
    ]
    floating = [
        ("Birthday of Martin Luther King, Jr.", nth_weekday(year, 1, MONDAY, 3)),
        ("Washington's Birthday (Presidents Day)", nth_weekday(year, 2, MONDAY, 3)),
        ("Memorial Day", last_weekday(year, 5, MONDAY)),
        ("Labor Day", nth_weekday(year, 9, MONDAY, 1)),
        ("Columbus Day", nth_weekday(year, 10, MONDAY, 2)),
        ("Thanksgiving Day", nth_weekday(year, 11, THURSDAY, 4)),
    ]
    out = [(n, d, observed(d)) for n, d in fixed]
    out += [(n, d, d) for n, d in floating]
    out.sort(key=lambda r: r[1])
    return out


def easter(year):
    """Easter Sunday, anonymous Gregorian algorithm (Meeus/Jones/Butcher)."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return date(year, month, day + 1)


def easter_related(year):
    """Ash Wednesday (46 days before), Palm Sunday (7 before), Good Friday (2 before)."""
    e = easter(year)
    return [
        ("Ash Wednesday", e - timedelta(days=46)),
        ("Palm Sunday", e - timedelta(days=7)),
        ("Good Friday", e - timedelta(days=2)),
    ]


def dst_us(year):
    """US daylight saving time (since 2007): second Sunday of March,
    first Sunday of November."""
    return nth_weekday(year, 3, SUNDAY, 2), nth_weekday(year, 11, SUNDAY, 1)


def _fmt(d):
    return d.strftime("%a %b %d, %Y")


def render(year):
    lines = [f"US holidays {year}", ""]
    lines.append(f"{'Federal holiday':<42}{'Actual':<18}Observed")
    for name, actual, obs in federal_holidays(year):
        lines.append(f"{name:<42}{_fmt(actual):<18}{_fmt(obs)}")
    lines += ["", f"{'Easter-related':<42}Date"]
    lines.append(f"{'Easter Sunday':<42}{_fmt(easter(year))}")
    for name, d in easter_related(year):
        lines.append(f"{name:<42}{_fmt(d)}")
    start, end = dst_us(year)
    lines += ["", f"{'Daylight saving time':<42}Date",
              f"{'DST starts (clocks forward)':<42}{_fmt(start)}",
              f"{'DST ends (clocks back)':<42}{_fmt(end)}"]
    return "\n".join(lines)


def main(argv):
    if len(argv) != 2:
        print("usage: python us_holidays.py YEAR", file=sys.stderr)
        return 2
    try:
        year = int(argv[1])
    except ValueError:
        print("YEAR must be an integer", file=sys.stderr)
        return 2
    if not 1971 <= year <= 9998:
        print("YEAR must be between 1971 and 9998", file=sys.stderr)
        return 2
    print(render(year))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
