# TODO Add license header

from fuzzy_clock.main import _convert_hour_to_word
from fuzzy_clock.main import _convert_minute_to_word
from fuzzy_clock.main import _increment_hour
from fuzzy_clock.main import _is_half_past_hour
from fuzzy_clock.main import to_fuzzy_time
from hypothesis import given
from hypothesis.strategies import integers, just, sampled_from
from unittest import TestCase

EXPECTED_MINUTE_WORDS = {
    5: {
        "": [1, 2, 3, 4],
        "five": [5, 6, 7, 8, 9, 55, 56, 57, 58, 59],
        "ten": [10, 11, 12, 13, 14, 50, 51, 52, 53, 54],
        "quarter": [15, 16, 17, 18, 19, 45, 46, 47, 48, 49],
        "twenty": [20, 21, 22, 23, 24, 40, 41, 42, 43, 44],
        "twenty-five": [25, 26, 27, 28, 29, 35, 36, 37, 38, 39],
        "half": [30, 31, 32, 33, 34]
    },
    10: {
        "": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "ten": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
        "twenty": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                   40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        "half": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
    },
    15: {
        "": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
             11, 12, 13, 14],
        "quarter": [15, 16, 17, 18, 19, 20,
                    21, 22, 23, 24, 25, 26, 27, 28, 29,
                    45, 46, 47, 48, 49,
                    50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
        "half": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                 40, 41, 42, 43, 44]
    }
}


EXPECTED_HOURS_WORDS = {
    "midnight": [0],
    "one": [1, 13],
    "two": [2, 14],
    "three": [3, 15],
    "four": [4, 16],
    "five": [5, 17],
    "six": [6, 18],
    "seven": [7, 19],
    "eight": [8, 20],
    "nine": [9, 21],
    "ten": [10, 22],
    "eleven": [11, 23],
    "noon": [12]
}

EXPECTED_ON_HOUR_RESULTS = {
    0: "midnight",
    1: "one o'clock",
    2: "two o'clock",
    3: "three o'clock",
    4: "four o'clock",
    5: "five o'clock",
    6: "six o'clock",
    7: "seven o'clock",
    8: "eight o'clock",
    9: "nine o'clock",
    10: "ten o'clock",
    11: "eleven o'clock",
    12: "noon",
    13: "one o'clock",
    14: "two o'clock",
    15: "three o'clock",
    16: "four o'clock",
    17: "five o'clock",
    18: "six o'clock",
    19: "seven o'clock",
    20: "eight o'clock",
    21: "nine o'clock",
    22: "ten o'clock",
    23: "eleven o'clock"
}


class MainTest(TestCase):

    @given(integers(min_value=0, max_value=59), sampled_from([5, 10, 15]))
    def test_convert_minutes_to_word(self, minute, resolution):
        result = _convert_minute_to_word(minute, resolution)

        self.assertIsNotNone(result)
        self.assertIn(result, EXPECTED_MINUTE_WORDS[resolution])


    @given(integers(min_value=0, max_value=23))
    def test_convert_hour_to_word(self, hour):
        result = _convert_hour_to_word(hour)

        self.assertIsNotNone(result)
        self.assertIn(hour, EXPECTED_HOURS_WORDS[result])

    @given(integers(min_value=0, max_value=23))
    def test_increment_hour(self, hour):
        result = _increment_hour(hour)

        if (hour < 23):
            self.assertEquals(result, hour + 1)
        else:
            self.assertEquals(result, 0)


    @given(integers(min_value=0, max_value=59), sampled_from([5, 10, 15]))
    def test_is_half_past_hour(self, minutes, resolution):
        result = _is_half_past_hour(minutes, resolution)

        if (minutes >= 30 + resolution):
            self.assertTrue(result)
        else:
            self.assertFalse(result)


    @given(integers(min_value=0, max_value=23),
           integers(min_value=0, max_value=4),
           just(5))
    def test_fuzzy_time_on_the_hour_five_resolution(self, hour, minutes, resolution):
        result = to_fuzzy_time(hour, minutes, resolution)

        self.assertIsNotNone(result)
        self.assertEquals(result, EXPECTED_ON_HOUR_RESULTS[hour])


    @given(integers(min_value=0, max_value=23),
           integers(min_value=0, max_value=9),
           just(10))
    def test_fuzzy_time_on_the_hour_ten_resolution(self, hour, minutes, resolution):
        result = to_fuzzy_time(hour, minutes, resolution)

        self.assertIsNotNone(result)
        self.assertEquals(result, EXPECTED_ON_HOUR_RESULTS[hour])


    @given(integers(min_value=0, max_value=23),
           integers(min_value=0, max_value=14))
    def test_fuzzy_time_on_the_hour_fifteen_resolution(self, hour, minutes):
        result = to_fuzzy_time(hour, minutes, 15)

        self.assertIsNotNone(result)
        self.assertEquals(result, EXPECTED_ON_HOUR_RESULTS[hour])


    @given(integers(min_value=0, max_value=23),
           integers(min_value=5, max_value=34),
           just(5))
    def test_fuzzy_time_during_the_first_half_hour_five_resolution(self, hour, minutes, resolution):
        result = to_fuzzy_time(hour, minutes, resolution)

        expected_hour = _convert_hour_to_word(hour)
        expected_minute = _convert_minute_to_word(minutes, resolution)

        self.assertIsNotNone(result)
        self.assertEquals(result, " ".join([expected_minute, "past", expected_hour]))


    @given(integers(min_value=0, max_value=23),
           integers(min_value=10, max_value=39),
           just(10))
    def test_fuzzy_time_during_the_first_half_hour_ten_resolution(self, hour, minutes, resolution):
        result = to_fuzzy_time(hour, minutes, resolution)

        expected_hour = _convert_hour_to_word(hour)
        expected_minute = _convert_minute_to_word(minutes, resolution)

        self.assertIsNotNone(result)
        self.assertEquals(result, " ".join([expected_minute, "past", expected_hour]))


    @given(integers(min_value=0, max_value=23),
           integers(min_value=15, max_value=44),
           just(15))
    def test_fuzzy_time_during_the_first_half_hour_fifteen_resolution(self, hour, minutes, resolution):
        result = to_fuzzy_time(hour, minutes, resolution)

        expected_hour = _convert_hour_to_word(hour)
        expected_minute = _convert_minute_to_word(minutes, resolution)

        self.assertIsNotNone(result)
        self.assertEquals(result, " ".join([expected_minute, "past", expected_hour]))


    @given(integers(min_value=0, max_value=23),
           integers(min_value=35, max_value=59),
           just(5))
    def test_fuzzy_time_during_the_last_half_hour_five_resolution(self, hour, minutes, resolution):
        result = to_fuzzy_time(hour, minutes, resolution)

        expected_hour = _convert_hour_to_word(_increment_hour(hour))
        expected_minute = _convert_minute_to_word(minutes, resolution)

        self.assertIsNotNone(result)
        self.assertEquals(result, " ".join([expected_minute, "till", expected_hour]))


    @given(integers(min_value=0, max_value=23),
           integers(min_value=40, max_value=59),
           just(10))
    def test_fuzzy_time_during_the_last_half_hour_ten_resolution(self, hour, minutes, resolution):
        result = to_fuzzy_time(hour, minutes, resolution)

        expected_hour = _convert_hour_to_word(_increment_hour(hour))
        expected_minute = _convert_minute_to_word(minutes, resolution)

        self.assertIsNotNone(result)
        self.assertEquals(result, " ".join([expected_minute, "till", expected_hour]))


    @given(integers(min_value=0, max_value=23),
           integers(min_value=45, max_value=59),
           just(15))
    def test_fuzzy_time_during_the_last_half_hour_ten_resolution(self, hour, minutes, resolution):
        result = to_fuzzy_time(hour, minutes, resolution)

        expected_hour = _convert_hour_to_word(_increment_hour(hour))
        expected_minute = _convert_minute_to_word(minutes, resolution)

        self.assertIsNotNone(result)
        self.assertEquals(result, " ".join([expected_minute, "till", expected_hour]))
