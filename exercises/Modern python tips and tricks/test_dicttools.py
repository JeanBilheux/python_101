import unittest

from dicttools import flatten_dict, pluck


class FlattenDictTests(unittest.TestCase):

    """Tests for flatten_dict."""

    flavors = {
        'savory': {
            'green': ['edamame', 'seaweed', 'wasabi'],
            'brown': ['peanut', 'bacon'],
        },
        'sweet': {
            'green': ['durian'],
            'pink': ['watermelon', 'strawberry'],
            'purple': ['blueberry', 'taro'],
        },
        'bitter': {
            'green': ['kale', 'arugula'],
        },
    }
    flattened_flavors = {
        'savory_green': ['edamame', 'seaweed', 'wasabi'],
        'savory_brown': ['peanut', 'bacon'],
        'sweet_green': ['durian'],
        'sweet_pink': ['watermelon', 'strawberry'],
        'sweet_purple': ['blueberry', 'taro'],
        'bitter_green': ['kale', 'arugula'],
    }

    def test_flattening_empty_dict(self):
        self.assertEqual(flatten_dict({}), {})

    def test_flattening_dict_of_dicts(self):
        flavors = self.flavors.copy()
        self.assertEqual(flatten_dict(flavors), self.flattened_flavors)

    def test_original_dict_not_changed(self):
        flavors = self.flavors.copy()
        flatten_dict(flavors)
        self.assertEqual(flavors, self.flavors)

    def test_flattening_does_not_copy(self):
        original = {'a': {'b': object()}}
        flattened = flatten_dict(original)
        self.assertIs(flattened['a_b'], original['a']['b'])

    def test_flatten_with_non_strings(self):
        self.assertEqual(
            flatten_dict({'a': {1: True, 2: False}, 'b': {3: True, 4: False}}),
            {'a_1': True, 'a_2': False, 'b_3': True, 'b_4': False},
        )

    def test_empty_nested_dictionaries_ignored(self):
        self.assertEqual(
            flatten_dict({'a': {'z': 8}, 'b': {}}),
            {'a_z': 8},
        )

    def test_specifying_separator(self):
        self.assertEqual(
            flatten_dict({'a': {'b': 'x'}, 'd': {'e': 'y'}}, sep='.'),
            {'a.b': 'x', 'd.e': 'y'},
        )
        self.assertEqual(flatten_dict({}, sep='.'), {})
        with self.assertRaises(TypeError):
            flatten_dict({}, '.')

    def test_non_dictionaries_allowed(self):
        self.assertEqual(
            flatten_dict({'A': 'a', 'B': 'b', 'C': 'c'}),
            {'A': 'a', 'B': 'b', 'C': 'c'},
        )
        self.assertEqual(
            flatten_dict({'a': {'b': 5, 'z': 20}, 'c': {'d': 3}, 'x': 40}),
            {'a_b': 5, 'a_z': 20, 'c_d': 3, 'x': 40},
        )
        self.assertEqual(
            flatten_dict({'1': [], '2': {}, '3': ()}),
            {'1': [], '3': ()},
        )

    def test_arbitrarily_deep_flattening(self):
        self.assertEqual(
            flatten_dict({
                'a': {
                    'v': 0,
                    'b': {'c': {'w': 1, 'd': {'e': 2, 'x': 3}}, 'y': 4},
                },
                'z': 5,
            }), {
                'a_v': 0,
                'a_b_c_w': 1,
                'a_b_c_d_e': 2,
                'a_b_c_d_x': 3,
                'a_b_y': 4,
                'z': 5,
            },
        )
        self.assertEqual(
            flatten_dict({
                'a': {
                    'v': 0,
                    'b': {'c': {'w': 1, 'd': {'e': 2, 'x': 3}}, 'y': 4},
                },
                'z': 5,
            }, sep=', '), {
                'a, v': 0,
                'a, b, c, w': 1,
                'a, b, c, d, e': 2,
                'a, b, c, d, x': 3,
                'a, b, y': 4,
                'z': 5,
            },
        )


class PluckTests(unittest.TestCase):

    """Tests for pluck."""

    def test_pluck_top_level(self):
        d = {'a': {'b': 5, 'z': 20}, 'c': {'d': 3}, 'x': 40}
        self.assertEqual(pluck(d, 'x'), 40)
        self.assertEqual(pluck(d, 'c'), {'d': 3})

    def test_pluck_one_level_deep(self):
        d = {'a': {'b': 5, 'z': 20}, 'c': {'d': 3}, 'x': 40}
        self.assertEqual(pluck(d, 'a.b'), 5)
        self.assertEqual(pluck(d, 'c.d'), 3)

    def test_pluck_many_levels_deep(self):
        d = {'a': {'b': {'c': {'d': {'e': 4}}}}}
        self.assertEqual(pluck(d, 'a.b.c'), {'d': {'e': 4}})
        self.assertEqual(pluck(d, 'a.b.c.d'), {'e': 4})
        self.assertEqual(pluck(d, 'a.b.c.d.e'), 4)

    def test_exception_on_missing_item(self):
        d = {'a': {'b': 5, 'z': 20}, 'c': {'d': 3}, 'x': 40}
        with self.assertRaises(KeyError):
            pluck(d, 'c.e')
        with self.assertRaises(KeyError):
            pluck(d, 'z')

    def test_specifying_separator(self):
        d = {'a': {'b': 5, 'z': 20}, 'c': {'d': 3}, 'x': 40}
        self.assertEqual(pluck(d, 'c/d', sep='/'), 3)
        self.assertEqual(pluck(d, 'a.b', sep='.'), 5)
        self.assertEqual(pluck(d, 'a z', sep=' '), 20)

    def test_specifying_default_value(self):
        d = {'a': {'b': 5, 'z': 20}, 'c': {'d': 3}, 'x': 40}
        self.assertEqual(pluck(d, 'c.e', default=None), None)
        self.assertEqual(pluck(d, 'y.z', default=0), 0)

    def test_multiple_lookups_accepted(self):
        d = {'a': {'b': 5, 'z': 20}, 'c': {'d': 3}, 'x': 40}
        self.assertEqual(
            pluck(d, 'a.b', 'c.e', 'c.d', 'x', default=None),
            (5, None, 3, 40),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
