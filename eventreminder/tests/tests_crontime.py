import unittest

from eventreminder.crontime import CronTime


class MyTestCase(unittest.TestCase):

    def test_eq_simple(self):
        c1 = CronTime('*', '*', '*')
        c2 = CronTime('*', '*', '*')
        c3 = CronTime('1', '*', '*')
        self.assertNotEqual(c1, 'Hello world')
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)

    def test_eq_deep(self):
        c1 = CronTime('*', '*', '*')
        c2 = CronTime('*', '*/1', '*')
        c3 = CronTime('*', '*/2', '*')
        c4 = CronTime('*', '2,4,6,8,10,12', '*')
        c5 = CronTime('*', '2,4,6,8,12,*/10', '*')
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)
        self.assertEqual(c3, c4)
        self.assertEqual(c3, c5)
        c6 = CronTime('0/15', '9-12', '0,6')
        c7 = CronTime('15,30', '9/12,*/10,*/11,12', '0/6')
        self.assertEqual(c6, c7)
        c8 = CronTime('*', '1/2', '0/2')
        c9 = CronTime('1-31', '1/4,3/4', '0/4,2/4')
        self.assertEqual(c8, c9)

    def test_str(self):
        c1 = CronTime('2-5,*/11,3/11', '6', '*')
        c2 = CronTime('10', '*/4', '*')
        c3 = CronTime('*', '*', '*')
        self.assertEqual("2-5,*/11,3/11 6 *", str(c1))
        self.assertEqual("10 */4 *", str(c2))
        self.assertEqual("* * *", str(c3))

    def test_repr(self):
        c1 = CronTime('2-5,*/10,3/10', '6', '*')
        c2 = CronTime('10', '*/4', '*')
        c3 = CronTime('*', '*/3', '*')
        c4 = CronTime('5', '5', '5')
        self.assertEqual("CronTime('2-5,*/10,3/10', '6', '*')", repr(c1))
        self.assertEqual("CronTime('10', '*/4', '*')", repr(c2))
        self.assertEqual("CronTime('*', '*/3', '*')", repr(c3))
        self.assertEqual("CronTime('5', '5', '5')", repr(c4))

    def test_is_time(self):
        c1 = CronTime('2-5,*/11,3/11', '1-3,6', '0-5')
        self.assertTrue(c1.is_time(4, 6, 0))
        self.assertTrue(c1.is_time(11, 1, 1))
        self.assertTrue(c1.is_time(14, 2, 2))
        self.assertTrue(c1.is_time(5, 3, 3))
        self.assertTrue(c1.is_time(22, 1, 4))
        self.assertTrue(c1.is_time(25, 2, 5))

        self.assertFalse(c1.is_time(1, 3, 0))
        self.assertFalse(c1.is_time(2, 4, 0))
        self.assertFalse(c1.is_time(5, 6, 6))
        self.assertFalse(c1.is_time(1, 4, 0))
        self.assertFalse(c1.is_time(1, 3, 6))
        self.assertFalse(c1.is_time(5, 4, 6))
        self.assertFalse(c1.is_time(15, 4, 6))

    def test_from_string_error(self):
        s_short = '* *'
        s_long = '* * * *'
        with self.assertRaises(AttributeError):
            CronTime.from_string(s_short)
        with self.assertRaises(AttributeError):
            CronTime.from_string(s_long)
        s_day = ['0 * *', '32 * *', '11-10 * *', '0-10 * *', '1-23/2 * *', 'a * *', '101/2 * *', '00/5 * *', '02 * *',
                 '08-14 * *', '2//4 * *', '15-40 * *', '-8 * *', '1-5,02 * *', '*,22-33 * *']
        for d in s_day:
            with self.assertRaises(AttributeError):
                CronTime.from_string(d)
        s_month = ['* 0 *', '* 13 *', '* 5-15 *', '* 0-18 *']
        for m in s_month:
            with self.assertRaises(AttributeError):
                CronTime.from_string(m)
        s_weekday = ['* * 7', '* * 10', '* * 3-10', '* * 0-7']
        for w in s_weekday:
            with self.assertRaises(AttributeError):
                CronTime.from_string(w)

    def test_from_string(self):
        self.assertEqual(CronTime('*', '*', '*'), CronTime.from_string('   *      * * '))
        self.assertEqual(CronTime('1-3,2/4,15', '3/5', '0,1,2'), CronTime.from_string('1-3,2/4,15   3/5 0,1,2   '))


if __name__ == '__main__':
    unittest.main()
