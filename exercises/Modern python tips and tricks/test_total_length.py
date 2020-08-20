import unittest

from total_length import total_length


class TotalLengthTests(unittest.TestCase):

    """Tests for total_length."""

    def test_list(self):
        self.assertEqual(total_length([1, 2, 3]), 3)

    def test_multiple_lists(self):
        self.assertEqual(total_length([1, 2, 3], [6, 7], [], [1]), 6)

    def test_sets(self):
        self.assertEqual(total_length({'hi', 'hello'}, {'yellow'}), 3)

    def test_mixed_iterables(self):
        self.assertEqual(total_length('hi', [0, 9], {1: 2}, {3, 8}, (2,)), 8)

    def test_nothing(self):
        self.assertEqual(total_length(), 0)

    # To test the Bonus part of this exercise, comment out the following line
    @unittest.expectedFailure
    def test_things_without_length(self):
        self.assertEqual(total_length([1, 2, 3], [4, 5], iter([6, 7])), 7)

    # To test the Bonus part of this exercise, comment out the following line
    @unittest.expectedFailure
    def test_tries_len_first(self):
        things = LengthLiar([1, 2], 10)
        things2 = LengthLiar([100, 50, 20, 30, 10], 0)
        self.assertEqual(total_length(things, things2), 10)
        self.assertEqual(
            total_length((n**2 for n in range(1000)), range(1000000000)),
            1000001000,
        )

    # To test the Bonus part of this exercise, comment out the following line
    @unittest.expectedFailure
    def test_use_length_hints(self):
        things = LengthHinter([1, 2], 10)
        things2 = LengthHinter([100, 50, 20, 30, 10], 0)
        self.assertEqual(total_length(things, things, use_hints=True), 20)
        self.assertEqual(total_length(things2, things2, use_hints=True), 10)
        self.assertEqual(total_length(things, things2, use_hints=True), 15)
        self.assertEqual(total_length(things, things2), 7)
        self.assertEqual(total_length(things, things2, use_hints=False), 7)
        self.assertEqual(
            total_length(reversed(range(1000000000)), use_hints=True),
            1000000000,
        )


class LengthLiar:
    def __init__(self, items, purported_length):
        self.length = purported_length
        self.items = items
    def __iter__(self):
        yield from self.items
    def __len__(self):
        return self.length


class LengthHinter:
    def __init__(self, items, hinted_length):
        self.length = hinted_length
        self.items = items
    def __iter__(self):
        yield from self.items
    def __length_hint__(self):
        return self.length


if __name__ == "__main__":
    unittest.main(verbosity=2)
