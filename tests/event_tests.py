import unittest

from src.event import Event


class EventTests(unittest.TestCase):

    def test_eq(self):
        e1 = Event("a", "b", "c")
        e2 = Event("a", "b")
        e3 = Event("x", "y")
        e4 = Event("x", "y", '')
        self.assertNotEqual(e1, 'Hello world')
        self.assertEqual(e3, e4)
        self.assertNotEqual(e1, e2)
        self.assertNotEqual(e1, e3)
        self.assertNotEqual(e2, e3)

    def test_str(self):
        e1 = Event("a", "b", "c")
        e2 = Event("a", "b")
        self.assertEqual("a; b; c", str(e1))
        self.assertEqual("a; b", str(e2))

    def test_repr(self):
        e1 = Event("a", "b", "c")
        e2 = Event("a", "b")
        self.assertEqual("Event('a', 'b', 'c')", repr(e1))
        self.assertEqual("Event('a', 'b', '')", repr(e2))

    def test_to_text(self):
        e1 = Event("a", "b", "c")
        e2 = Event("a", "b")
        self.assertEqual('a:\n\tb\n\tc', e1.to_text())
        self.assertEqual('a:\n\tb', e2.to_text())

    def test_error_from_string(self):
        s_short = 'a'
        s_empty = 'a;  ;  '
        s_long = 'a; b; c; d'
        with self.assertRaises(AttributeError):
            Event.from_string(s_short)
        with self.assertRaises(AttributeError):
            Event.from_string(s_empty)
        with self.assertRaises(AttributeError):
            Event.from_string(s_long)

    def test_from_string(self):
        s_skip2 = 'a; ; c;'
        self.assertEqual(Event('a', 'c'), Event.from_string(s_skip2))
        s_skip3 = 'a; ; c; d'
        self.assertEqual(Event('a', 'c', 'd'), Event.from_string(s_skip3))
        s = 'a;b;c'
        self.assertEqual(Event('a', 'b', 'c'), Event.from_string(s))
        s_spaces = '   a    ;    b    ;    c     '
        self.assertEqual(Event('a', 'b', 'c'), Event.from_string(s_spaces))
        s_empty = 'a; b;;;   c   ; ; ;'
        self.assertEqual(Event('a', 'b', 'c'), Event.from_string(s_empty))


if __name__ == '__main__':
    unittest.main()
