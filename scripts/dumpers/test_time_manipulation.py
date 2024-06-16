import unittest

import time_manipulation


class TestTimeManiuplation(unittest.TestCase):

    def test_conversion_no_month_flip(self):
        start_date = "20240511"
        start_time = "24:13:00"
        
        new_time, new_date = time_manipulation.normalize_time(
            start_time, start_date
        )

        self.assertEqual("20240512", new_date)
        self.assertEqual("00:13:00", new_time)

    def test_conversion_month_flip(self):
        start_date = "20240531"
        start_time = "25:13:00"

        new_time, new_date = time_manipulation.normalize_time(
            start_time, start_date
        )

        self.assertEqual("20240601", new_date)
        self.assertEqual("01:13:00", new_time)

    def test_no_conversion(self):
        start_date = "20240511"
        start_time = "13:13:00"

        new_time, new_date = time_manipulation.normalize_time(
            start_time, start_date
        )

        self.assertEqual(start_date, new_date)
        self.assertEqual(start_time, new_time)


if __name__ == "__main__":
    unittest.main()