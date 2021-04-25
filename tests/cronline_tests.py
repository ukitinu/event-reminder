import unittest

from src.cronline import CronLine
from src.crontime import CronTime
from src.event import Event


class MyTestCase(unittest.TestCase):

    def test_from_string(self):
        self.assertEqual(
            CronLine(CronTime('*', '*', '*'), Event('hello', 'world')),
            CronLine.from_string(' *   * * hello; world')
        )
        self.assertEqual(
            CronLine.from_string(' *   * * hello; world'),
            CronLine.from_string(' *   * * hello; world #simple example with comment')
        )
        self.assertEqual(
            CronLine(CronTime('1-20,0/25', '0/2', '*'), Event('unit', 'test', 'here')),
            CronLine.from_string(' 1-20,0/25 0/2 * unit; test ;here')
        )
        self.assertEqual(None, CronLine.from_string(' #this is a comment'))
        self.assertEqual(None, CronLine.from_string('  '))
        with self.assertRaises(AttributeError):
            CronLine.from_string(' *    *  * ')
        with self.assertRaises(AttributeError):
            CronLine.from_string(' 1-20,0/25        * unit;  test ;here')


if __name__ == '__main__':
    unittest.main()
