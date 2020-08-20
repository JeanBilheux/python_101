"""Tests for star exercises"""
from contextlib import redirect_stdout
from io import StringIO
import unittest


from stars import dict_from_tuple, print


class DictFromTupleTests(unittest.TestCase):

    """Tests for dict_from_tuple."""

    def test_four_items(self):
        inputs = [(1, 2, 3, 4), (5, 6, 7, 8)]
        outputs = {1: (2, 3, 4), 5: (6, 7, 8)}
        self.assertEqual(dict_from_tuple(inputs), outputs)

    def test_three_items(self):
        inputs = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        outputs = {1: (2, 3), 4: (5, 6), 7: (8, 9)}
        self.assertEqual(dict_from_tuple(inputs), outputs)


class PrintTests(unittest.TestCase):

    """Tests for print."""

    def test_print_one_argument(self):
        with redirect_stdout(StringIO()) as stdout:
            print("hi")
            print(4)
        self.assertEqual(stdout.getvalue(), "hi\n4\n")

    def test_print_with_multiple_arguments(self):
        with redirect_stdout(StringIO()) as stdout:
            print("hello", "there")
            print("I", "have", 4, "chickens")
        self.assertEqual(stdout.getvalue(), "hello there\nI have 4 chickens\n")

    def test_with_sep(self):
        with redirect_stdout(StringIO()) as stdout:
            print("Trey", "Diane", sep=", ")
            print("hello", "there", sep="\n")
        self.assertEqual(stdout.getvalue(), "Trey, Diane\nhello\nthere\n")

    def test_with_end(self):
        with redirect_stdout(StringIO()) as stdout:
            print(4, end='\n\n')
            print("hi", end='')
        self.assertEqual(stdout.getvalue(), "4\n\nhi")

    def test_with_sep_and_end(self):
        with redirect_stdout(StringIO()) as stdout:
            print(*range(5), sep=",", end="!")
        self.assertEqual(stdout.getvalue(), "0,1,2,3,4!")


if __name__ == "__main__":
    unittest.main(verbosity=2)
