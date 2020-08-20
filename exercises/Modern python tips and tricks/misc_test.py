"""Tests for miscellaneous exercises"""
from collections.abc import Mapping, Iterable
from sys import getsizeof
from time import perf_counter
import unittest


from helpers import Mock
from misc import count_calls, deep_flatten, PermaDict, OrderedSet, CyclicList


class CountCallsTests(unittest.TestCase):

    """Tests for count_calls."""

    def test_count_increments(self):
        func = Mock()
        func.__name__ = "func"
        decorated = count_calls(func)
        func.assert_not_called()
        decorated()
        func.assert_called_once_with(1)
        decorated()
        func.assert_called_with(2)

    def test_return_value(self):
        def one(count): return 1
        one = count_calls(one)
        self.assertEqual(one(), 1)

    def test_takes_arguments(self):
        def add(count, x, y): return x + y
        add = count_calls(add)
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(1, 3), 4)


class DeepFlattenTests(unittest.TestCase):

    """Tests for deep_flatten."""

    def test_deep_lists(self):
        inputs = [0, [1, [2, 3]], [4]]
        outputs = [0, 1, 2, 3, 4]
        self.assertEqual(list(deep_flatten(inputs)), outputs)

    def test_empty_deep_list(self):
        self.assertEqual(list(deep_flatten([[()]])), [])


class OrderedSetTests(unittest.TestCase):

    """Tests for OrderedSet."""

    def test_constructor(self):
        OrderedSet([1, 2, 3, 4])

    def test_iterable(self):
        numbers = OrderedSet([1, 2, 3, 4])
        self.assertEqual(set(numbers), {1, 2, 3, 4})

    def test_uniqueness(self):
        numbers = OrderedSet([1, 3, 2, 4, 2, 1, 4, 5])
        self.assertEqual(sorted(numbers), [1, 2, 3, 4, 5])

    def test_maintains_order_and_uniqueness(self):
        string = "Hello world.  This string contains many characters in it."
        expected = "Helo wrd.Thistngcamy"
        characters = OrderedSet(string)
        self.assertEqual("".join(characters), expected)

    def test_length(self):
        numbers = OrderedSet([1, 2, 4, 2, 1, 4, 5])
        self.assertEqual(len(numbers), 4)
        self.assertEqual(len(OrderedSet('hiya')), 4)
        self.assertEqual(len(OrderedSet('hello there')), 7)

    def test_containment(self):
        numbers = OrderedSet([1, 2, 4, 2, 1, 4, 5])
        self.assertIn(2, numbers)
        self.assertNotIn(3, numbers)

    def test_memory_and_time_efficient(self):
        with Timer() as small_set_timer:
            numbers = OrderedSet([9999 for _ in range(2000)])
        with Timer() as large_set_timer:
            numbers2 = OrderedSet([9999 + i for i in range(2000)])

        # Time efficient construction
        self.assertGreater(
            small_set_timer.elapsed * 5,
            large_set_timer.elapsed,
        )

        # Memory efficient
        self.assertLess(get_size(numbers) * 100, get_size(numbers2))
        self.assertLess(get_size(numbers), 2000)

        with Timer() as beginning_lookup:
            9999 in numbers2
        with Timer() as end_lookup:
            -1 in numbers2

        # Time efficient lookups
        self.assertGreater(
            beginning_lookup.elapsed * 1.5,
            end_lookup.elapsed,
        )

    def test_add_and_discard(self):
        numbers = OrderedSet([1, 2, 3])
        numbers.add(3)
        self.assertEqual(len(numbers), 3)
        numbers.add(4)
        self.assertEqual(len(numbers), 4)
        numbers.discard(4)
        self.assertEqual(len(numbers), 3)
        numbers.discard(4)
        self.assertEqual(len(numbers), 3)
        with self.assertRaises(KeyError):
            numbers.remove(4)
        numbers.remove(3)
        self.assertEqual(len(numbers), 2)
        numbers.clear()
        self.assertEqual(len(numbers), 0)


class PermaDictTests(unittest.TestCase):

    """Tests for PermaDict."""

    def test_can_add_key(self):
        d = PermaDict()
        with self.assertRaises(KeyError):
            d[4]
        d[4] = "the number four"
        self.assertEqual(d[4], "the number four")

    def test_equal_to_dict(self):
        d = PermaDict()
        self.assertNotEqual(d, {4: "the number four"})
        d[4] = "the number four"
        self.assertEqual(d, {4: "the number four"})
        self.assertNotEqual(d, {4: "the number five"})
        self.assertEqual(PermaDict({1: 2, 3: 4}), {1: 2, 3: 4})

    def test_can_iterate(self):
        d = PermaDict({'a': 'b', 'c': 'd'})
        self.assertEqual(set(d), {'a', 'c'})

    def test_has_keys_values_and_items(self):
        d = PermaDict({'a': 'b', 'c': 'd'})
        self.assertEqual(set(d.keys()), {'a', 'c'})
        self.assertEqual(set(d.values()), {'b', 'd'})
        self.assertEqual(set(d.items()), {('a', 'b'), ('c', 'd')})

    def test_can_pop_key(self):
        d = PermaDict()
        self.assertNotEqual(d, {4: "the number four"})
        d[4] = "the number four"
        self.assertEqual(d, {4: "the number four"})
        self.assertNotEqual(d, {4: "the number five"})

    def test_can_update_with_new_keys(self):
        d = PermaDict()
        d.update({'a': 1})
        self.assertEqual(d, {'a': 1})
        d.update([('b', 2)])
        self.assertEqual(d, {'a': 1, 'b': 2})
        d.update(c=3)
        self.assertEqual(d, {'a': 1, 'b': 2, 'c': 3})

    def test_error_when_changing_value(self):
        d = PermaDict()
        d[4] = "the number four"
        with self.assertRaises(KeyError):
            d[4] = "the number 4"
        self.assertEqual(d, {4: "the number four"})

    def test_error_when_updating_value(self):
        d = PermaDict({1: 2, 3: 4})
        with self.assertRaises(KeyError):
            d.update([(5, 6), (1, 8), (7, 8)])
        self.assertEqual(d, {1: 2, 3: 4, 5: 6})

    def test_setdefault(self):
        d = PermaDict()
        d.setdefault('a', 1)
        self.assertEqual(d, {'a': 1})
        d.setdefault('a', 2)
        self.assertEqual(d, {'a': 1})


class CyclicListTests(unittest.TestCase):

    """Tests for CyclicList."""

    def test_constructor(self):
        CyclicList([1, 2, 3, 4])

    def test_iterate_to_length(self):
        numbers = CyclicList([1, 2, 3])
        i = iter(numbers)
        self.assertEqual([next(i), next(i), next(i)], [1, 2, 3])

    def test_iterate_past_length(self):
        numbers = CyclicList([1, 2, 3])
        new_list = [x for x, _ in zip(numbers, range(10))]
        self.assertEqual(new_list, [1, 2, 3, 1, 2, 3, 1, 2, 3, 1])

    def test_length(self):
        numbers = CyclicList([1, 2, 3])
        self.assertEqual(len(numbers), 3)

    def test_append_and_pop(self):
        numbers = CyclicList([1, 2, 3])
        numbers.append(8)
        self.assertEqual(len(numbers), 4)
        self.assertEqual(numbers.pop(), 8)
        self.assertEqual(len(numbers), 3)

    @unittest.skip("Slicing not implemented")
    def test_slice(self):
        numbers = CyclicList([1, 2, 3])
        self.assertEqual(numbers[:5], [1, 2, 3, 1, 2])

    def test_index_before_length(self):
        numbers = CyclicList([1, 2, 3, 4])
        self.assertEqual(numbers[2], 3)

    def test_index_past_length(self):
        numbers = CyclicList([1, 2, 3, 4])
        self.assertEqual(numbers[4], 1)


def get_size(obj, seen=None):
    """Return size of any Python object."""
    if seen is None:
        seen = set()
    size = getsizeof(obj)
    if id(obj) in seen:
        return 0
    seen.add(id(obj))
    if hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    if hasattr(obj, '__slots__'):
        size += sum(
            get_size(getattr(obj, attr), seen)
            for attr in obj.__slots__
            if hasattr(obj, attr)
        )
    if isinstance(obj, Mapping):
        size += sum(
            get_size(k, seen) + get_size(v, seen)
            for k, v in obj.items()
        )
    elif isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        size += sum(get_size(item, seen) for item in obj)
    return size


class Timer:

    """Context manager to time a code block."""

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, *args):
        self.end = perf_counter()
        self.elapsed = self.end - self.start



if __name__ == "__main__":
    unittest.main(verbosity=2)
