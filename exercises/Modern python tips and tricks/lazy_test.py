"""Tests for laziness exercises"""
import unittest


from lazy import reverse_difference, get_shared_keys


class ReverseDifferenceTests(unittest.TestCase):

    """Tests for reverse_difference."""

    def test_empty(self):
        self.assertEqual(reverse_difference([]), [])

    def test_one(self):
        self.assertEqual(reverse_difference([1]), [0])

    def test_two(self):
        self.assertEqual(reverse_difference([0, 0]), [0, 0])

    def test_three(self):
        self.assertEqual(reverse_difference([3, 2, 1]), [2, 0, -2])

    def test_four(self):
        self.assertEqual(reverse_difference([9, 8, 7, 6]), [3, 1, -1, -3])

    def test_five(self):
        inputs = [1, 2, 3, 4, 5]
        outputs = [-4, -2, 0, 2, 4]
        self.assertEqual(reverse_difference(inputs), outputs)


class GetSharedKeys(unittest.TestCase):

    """Tests for get_shared_keys."""

    def test_no_keys_in_common(self):
        d1 = {1: (2, 3), 4: (5, 6), 7: (8, 9)}
        d2 = {3: 0, 2: 9, 6: 4}
        self.assertEqual(set(get_shared_keys(d1, d2)), set())

    def test_some_shared_keys(self):
        d1 = {1: (2, 3), 4: (5, 6), 7: (8, 9)}
        d2 = {3: 0, 4: 9, 6: 4, 1: 7}
        self.assertEqual(set(get_shared_keys(d1, d2)), {4, 1})

    def test_with_strings(self):
        expired = {'c95': '20200315', 'd45': '20200401', 'b38': '20200415'}
        used_recently = {'a56': 8, 'b38': 1, 'e77': 4, 'd45': 3}
        expected = {'d45', 'b38'}
        self.assertEqual(set(get_shared_keys(expired, used_recently)), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
