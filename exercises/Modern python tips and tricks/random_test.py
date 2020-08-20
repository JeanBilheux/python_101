"""Tests for random exercises"""
import builtins
import unittest

from helpers import run_program, ModuleTestCase, make_file, Mock


class CapitalGuessing(ModuleTestCase):

    """
    Tests for guess_capitals.py

    Prompt user to guess capitals.
    """

    module_path = 'guess_capitals.py'

    def test_single_capital_correct_guess(self):
        calls = ['Capital']
        expected = "Correct! Capital is the capital of Place\n"
        builtins.input, old_input = Mock(side_effect=calls), builtins.input
        try:
            with make_file('state,capital\nPlace,Capital') as filename:
                output = run_program('guess_capitals.py', [filename])
        finally:
            mock_input, builtins.input = builtins.input, old_input
        mock_input.assert_called_once_with("What is the capital of Place? ")
        self.assertEqual(output, expected)

    def test_single_capital_incorrect_guess(self):
        calls = ['Wrong', 'Capital']
        expected = (
            "That's not correct.  Try again.\n"
            "Correct! Capital is the capital of Place\n"
        )
        builtins.input, old_input = Mock(side_effect=calls), builtins.input
        try:
            with make_file('state,capital\nPlace,Capital') as filename:
                output = run_program('guess_capitals.py', [filename])
        finally:
            mock_input, builtins.input = builtins.input, old_input
        mock_input.assert_called_with("What is the capital of Place? ")
        self.assertEqual(output, expected)

    def test_multiple_capitals(self):
        capital_data = 'state,capital\nPlace1,Capital1\nPlace2,Capital2'
        calls = ['Capital1', 'Capital2'] * 50
        not_correct = "That's not correct.  Try again.\n"
        correct1 = "Correct! Capital1 is the capital of Place1\n"
        correct2 = "Correct! Capital2 is the capital of Place2\n"
        expected = {
            not_correct + correct1,
            not_correct + correct2,
            correct1,
            correct2,
        }
        builtins.input, old_input = Mock(side_effect=calls), builtins.input
        try:
            with make_file(capital_data) as filename:
                outputs = {
                    run_program('guess_capitals.py', [filename])
                    for _ in range(50)
                }
        finally:
            mock_input, builtins.input = builtins.input, old_input
        mock_input.assert_any_call("What is the capital of Place1? ")
        mock_input.assert_any_call("What is the capital of Place2? ")
        self.assertEqual(outputs, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
