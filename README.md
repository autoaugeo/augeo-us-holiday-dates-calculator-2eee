# us-holidays

A small, dependency-free Python module that computes US holiday dates for any year:

- `federal_holidays(year)`: the 11 US federal holidays as `(name, actual date, observed date)`. Saturday holidays are observed on Friday, Sunday holidays on Monday (so New Year's Day 2028, a Saturday, is observed on Dec 31, 2027).
- `easter(year)`: Easter Sunday, using the anonymous Gregorian algorithm.
- `easter_related(year)`: Ash Wednesday, Palm Sunday and Good Friday.
- `dst_us(year)`: start (second Sunday of March) and end (first Sunday of November) of US daylight saving time, valid for 2007 onward.

## Usage

```
python us_holidays.py 2027
```

prints a table of federal holidays (actual and observed), Easter-related dates and DST dates. As a library:

```python
import us_holidays
us_holidays.easter(2027)   # datetime.date(2027, 3, 28)
us_holidays.dst_us(2027)   # (date(2027, 3, 14), date(2027, 11, 7))
```

Python 3, standard library only.

## Tests

```
python3 test_us_holidays.py
```

The tests check known dates for 2026, 2027 and 2028, for example Juneteenth 2027 observed Fri Jun 18, Christmas 2027 observed Fri Dec 24, Easter 2027 on Mar 28 and 2028 on Apr 16. The exit code is non-zero if any date is wrong.

## Printable calendar

The same logic feeds a free printable 2027 calendar with holidays: https://augeo-free-printable-2027-calendar-holidays-an-2eee.pages.dev/

## About

This project is built and maintained by an automated agent system.

Licensed under the MIT License (see `LICENSE`).
