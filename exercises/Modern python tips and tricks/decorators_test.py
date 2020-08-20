"""Tests for decorator exercises"""
import builtins
from io import StringIO
import sys
import unittest

from helpers import Mock
from decorators import catch_all


class CatchAllTests(unittest.TestCase):

    """Tests for catch_all."""

    def test_suppress_error(self):
        def divide(x, y): return x / y
        divide = catch_all(divide)
        sys.stdout, old_stdout = StringIO(), sys.stdout
        try:
            builtins.input, old_input = Mock(side_effect=['y']), builtins.input
            try:
                divide(1, 0)
            finally:
                mock_input, builtins.input = builtins.input, old_input
        finally:
            stdout, sys.stdout = sys.stdout, old_stdout
        self.assertEqual(
            stdout.getvalue().strip(),
            "Exception occurred: division by zero"
        )
        mock_input.assert_called_with("Should we ignore this exception (Y/n)? ")

    def test_do_not_suppress(self):
        def divide(x, y): return x / y
        divide = catch_all(divide)
        sys.stdout, old_stdout = StringIO(), sys.stdout
        try:
            builtins.input, old_input = Mock(side_effect=['n']), builtins.input
            try:
                with self.assertRaises(ZeroDivisionError):
                    divide(1, 0)
            finally:
                mock_input, builtins.input = builtins.input, old_input
        finally:
            stdout, sys.stdout = sys.stdout, old_stdout
        self.assertEqual(
            stdout.getvalue().strip(),
            "Exception occurred: division by zero"
        )
        mock_input.assert_called_with("Should we ignore this exception (Y/n)? ")

    def test_return_value(self):
        def one(): return 1
        one = catch_all(one)
        self.assertEqual(one(), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
