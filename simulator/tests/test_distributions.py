import unittest
from simulator.rhythms import apply_time_of_day, motion_probability

class TestRhythms(unittest.TestCase):
    def test_apply_time_of_day(self):
        # Monday 8am = morning_peak
        self.assertEqual(apply_time_of_day(8, 0), "morning_peak")
        # Saturday 8am = baseline
        self.assertEqual(apply_time_of_day(8, 5), "baseline")
        # Evening 7pm = evening_peak
        self.assertEqual(apply_time_of_day(19, 2), "evening_peak")

    def test_motion_prob(self):
        self.assertTrue(motion_probability("evening_peak") > motion_probability("baseline"))

if __name__ == '__main__':
    unittest.main()
