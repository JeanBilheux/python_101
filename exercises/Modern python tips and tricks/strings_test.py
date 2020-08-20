"""Tests for string exercises"""
import unittest

from strings import html_tag, dollars, split_in_half


class HTMLTagTests(unittest.TestCase):

    """Tests for html_tag."""

    def assertTagEqual(self, tag1, tag2):
        split1 = tag1[1:-1].split(' ')
        name1, attrs1 = split1[0], split1[1:]
        split2 = tag2[1:-1].split(' ')
        name2, attrs2 = split2[0], split2[1:]
        self.assertEqual(name1, name2)
        self.assertEqual(sorted(attrs1), sorted(attrs2))
        self.assertEqual(tag1[0], tag2[0])
        self.assertEqual(tag1[-1], tag2[-1])

    def test_input(self):
        html = html_tag("input", type="email", name="email",
                        placeholder="E-mail")
        expected = '<input name="email" placeholder="E-mail" type="email">'
        self.assertTagEqual(html, expected)

    def test_img(self):
        html = html_tag("img", src="https://placehold.it/10x10", alt="Sample")
        expected = '<img alt="Sample" src="https://placehold.it/10x10">'
        self.assertTagEqual(html, expected)


class DollarsTest(unittest.TestCase):

    """Tests for dollars."""

    def test_twelve_dollars(self):
        self.assertEqual(dollars(12), '$12.00')

    def test_three_dollars_fourty(self):
        self.assertEqual(dollars(3.4), '$3.40')

    def test_three_cents(self):
        self.assertEqual(dollars(.03), '$0.03')

    def test_fifty_cents(self):
        self.assertEqual(dollars(.5), '$0.50')

    def test_three_decimals(self):
        self.assertEqual(dollars(.008), '$0.01')


class HalfTests(unittest.TestCase):

    """Tests for split_in_half."""

    def test_even(self):
        self.assertEqual(split_in_half([1, 2, 3, 4]), ([1, 2], [3, 4]))

    def test_odd(self):
        self.assertEqual(split_in_half([1, 2, 3, 4, 5]), ([1, 2], [3, 4, 5]))

    def test_two(self):
        self.assertEqual(split_in_half([1, 2]), ([1], [2]))

    def test_empty(self):
        self.assertEqual(split_in_half([]), ([], []))

    def test_one(self):
        self.assertEqual(split_in_half([1]), ([], [1]))

    def test_string(self):
        self.assertEqual(split_in_half("Hello world!"), ('Hello ', 'world!'))

    def test_tuple(self):
        self.assertEqual(split_in_half((1, 2)), ((1,), (2,)))


if __name__ == "__main__":
    unittest.main()
