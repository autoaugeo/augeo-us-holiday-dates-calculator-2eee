import unittest
from datetime import date

import us_holidays as uh


def table(year):
    return {n: (a, o) for n, a, o in uh.federal_holidays(year)}


class FederalHolidays(unittest.TestCase):
    def test_eleven_holidays(self):
        for y in (2026, 2027, 2028):
            self.assertEqual(len(uh.federal_holidays(y)), 11)

    def test_2027_actual_dates(self):
        t = table(2027)
        self.assertEqual(t["New Year's Day"][0], date(2027, 1, 1))
        self.assertEqual(t["Birthday of Martin Luther King, Jr."][0], date(2027, 1, 18))
        self.assertEqual(t["Washington's Birthday (Presidents Day)"][0], date(2027, 2, 15))
        self.assertEqual(t["Memorial Day"][0], date(2027, 5, 31))
        self.assertEqual(t["Labor Day"][0], date(2027, 9, 6))
        self.assertEqual(t["Columbus Day"][0], date(2027, 10, 11))
        self.assertEqual(t["Veterans Day"][0], date(2027, 11, 11))
        self.assertEqual(t["Thanksgiving Day"][0], date(2027, 11, 25))

    def test_2027_observed(self):
        t = table(2027)
        self.assertEqual(t["Juneteenth National Independence Day"],
                         (date(2027, 6, 19), date(2027, 6, 18)))
        self.assertEqual(t["Independence Day"], (date(2027, 7, 4), date(2027, 7, 5)))
        self.assertEqual(t["Christmas Day"], (date(2027, 12, 25), date(2027, 12, 24)))

    def test_2026(self):
        t = table(2026)
        self.assertEqual(t["Birthday of Martin Luther King, Jr."][0], date(2026, 1, 19))
        self.assertEqual(t["Independence Day"], (date(2026, 7, 4), date(2026, 7, 3)))
        self.assertEqual(t["Thanksgiving Day"][0], date(2026, 11, 26))
        self.assertEqual(t["Christmas Day"], (date(2026, 12, 25), date(2026, 12, 25)))

    def test_2028(self):
        t = table(2028)
        self.assertEqual(t["New Year's Day"], (date(2028, 1, 1), date(2027, 12, 31)))
        self.assertEqual(t["Juneteenth National Independence Day"],
                         (date(2028, 6, 19), date(2028, 6, 19)))
        self.assertEqual(t["Thanksgiving Day"][0], date(2028, 11, 23))
        self.assertEqual(t["Memorial Day"][0], date(2028, 5, 29))


class EasterAndDst(unittest.TestCase):
    def test_easter(self):
        self.assertEqual(uh.easter(2026), date(2026, 4, 5))
        self.assertEqual(uh.easter(2027), date(2027, 3, 28))
        self.assertEqual(uh.easter(2028), date(2028, 4, 16))

    def test_easter_related(self):
        self.assertEqual(uh.easter_related(2027), [
            ("Ash Wednesday", date(2027, 2, 10)),
            ("Palm Sunday", date(2027, 3, 21)),
            ("Good Friday", date(2027, 3, 26))])
        self.assertEqual(uh.easter_related(2028), [
            ("Ash Wednesday", date(2028, 3, 1)),
            ("Palm Sunday", date(2028, 4, 9)),
            ("Good Friday", date(2028, 4, 14))])

    def test_dst(self):
        self.assertEqual(uh.dst_us(2026), (date(2026, 3, 8), date(2026, 11, 1)))
        self.assertEqual(uh.dst_us(2027), (date(2027, 3, 14), date(2027, 11, 7)))
        self.assertEqual(uh.dst_us(2028), (date(2028, 3, 12), date(2028, 11, 5)))


class Cli(unittest.TestCase):
    def test_render_contains_dates(self):
        out = uh.render(2027)
        self.assertIn("Fri Jun 18, 2027", out)
        self.assertIn("Sun Mar 28, 2027", out)


if __name__ == "__main__":
    unittest.main()
