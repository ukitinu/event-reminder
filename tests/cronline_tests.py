import unittest

from src.cronline import CronLine
from src.event import Event


class MyTestCase(unittest.TestCase):

    def test_eq_simple(self):
        c1 = CronLine('*', '*', '*', Event('a', 'b'))
        c2 = CronLine('*', '*', '*', Event('a', 'b', ''))
        c3 = CronLine('1', '*', '*', Event('a', 'b'))
        self.assertNotEqual(c1, 'Hello world')
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)

    def test_eq_deep(self):
        c1 = CronLine('*', '*', '*', Event('a', 'b'))
        c2 = CronLine('*', '*/1', '*', Event('a', 'b'))
        c3 = CronLine('*', '*/2', '*', Event('a', 'b'))
        c4 = CronLine('*', '2,4,6,8,10,12', '*', Event('a', 'b'))
        c5 = CronLine('*', '2,4,6,8,12,*/10', '*', Event('a', 'b'))
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)
        self.assertEqual(c3, c4)
        self.assertEqual(c3, c5)
        c6 = CronLine('0/15', '9-12', '0,6', Event('a', 'b'))
        c7 = CronLine('15,30', '9/12,*/10,*/11,12', '0/6', Event('a', 'b'))
        self.assertEqual(c6, c7)

    def test_str(self):
        c1 = CronLine('2-5,*/11,3/11', '6', '*', Event('a', 'b', 'c'))
        c2 = CronLine('10', '*/4', '*', Event('a', 'b'))
        c3 = CronLine('*', '*', '*', Event('a', 'b', 'c'))
        self.assertEqual("2-5,*/11,3/11 6 * a; b; c", str(c1))
        self.assertEqual("10 */4 * a; b", str(c2))
        self.assertEqual("* * * a; b; c", str(c3))

    def test_repr(self):
        c1 = CronLine('2-5,*/11,3/11', '6', '*', Event('a', 'b', 'c'))
        c2 = CronLine('10', '*/4', '*', Event('a', 'b'))
        c3 = CronLine('*', '*/3', '*', Event('a', 'b', 'c'))
        c4 = CronLine('5', '5', '5', Event('a', 'b'))
        self.assertEqual("CronLine('2-5,*/11,3/11', '6', '*', Event('a', 'b', 'c'))", repr(c1))
        self.assertEqual(f"CronLine('10', '*/4', '*', {repr(Event('a', 'b'))})", repr(c2))
        self.assertEqual("CronLine('*', '*/3', '*', Event('a', 'b', 'c'))", repr(c3))
        self.assertEqual(f"CronLine('5', '5', '5', {repr(Event('a', 'b'))})", repr(c4))


if __name__ == '__main__':
    unittest.main()
