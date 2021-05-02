import os
import unittest
from datetime import date

from eventreminder import reader
from eventreminder.event import Event

TEST_FILE = os.path.join(os.path.dirname(__file__), 'cron_events_test')


class MyTestCase(unittest.TestCase):
    def test_read_lines(self):
        today = date.today()
        day = today.day
        month = today.month
        weekday = today.weekday()

        errors = reader.read_lines(TEST_FILE, day, month, weekday).errors
        self.assertTrue(len(errors) == 1)
        self.assertTrue(9 in errors)

        events = reader.read_lines(TEST_FILE, day, month, weekday).events
        self.assertTrue(len(events) >= 2)
        self.assertTrue(Event('test', 'event') in events)
        self.assertTrue(Event('commented', 'event') in events)

        events = reader.read_lines(TEST_FILE, day, month, 7).events
        self.assertTrue(len(events) >= 3)
        self.assertTrue(Event('weekend', 'event') in events)

        events = reader.read_lines(TEST_FILE, 30, 2, 1).events
        self.assertTrue(len(events) >= 3)
        self.assertTrue(Event('impossible', 'event') in events)


if __name__ == '__main__':
    unittest.main()
