"""Tests for classes exercises"""
from contextlib import contextmanager
from datetime import date, timedelta
from locale import setlocale, LC_TIME
import unittest

from classes import (
    Point,
    BankAccount,
    MonthDelta,
    Month,
    Row,
    Node,
    DoublyLinkedNode,
)


class PointTests(unittest.TestCase):

    """Tests for Point."""

    def test_attributes(self):
        point = Point(1, 2, 3)
        self.assertEqual((point.x, point.y, point.z), (1, 2, 3))
        point.x = 4
        self.assertEqual(point.x, 4)

    def test_str(self):
        point = Point(1, 2, 3)
        self.assertEqual(str(point), 'Point(x=1, y=2, z=3)')
        self.assertEqual(repr(point), 'Point(x=1, y=2, z=3)')

    def test_equality(self):
        p1 = Point(1, 2, 3)
        p2 = Point(4, 5, 6)
        p3 = Point(1, 2, 3)
        self.assertEqual(p1, p3)
        self.assertNotEqual(p1, p2)
        self.assertTrue(p1 == p3)
        self.assertFalse(p1 != p3)
        self.assertFalse(p1 == p2)
        self.assertTrue(p1 != p2)
        self.assertFalse(p1 != p3)

    def test_magnitude(self):
        point = Point(2, 3, 6)
        self.assertEqual(point.magnitude, 7.0)
        point.y = 9
        self.assertEqual(point.magnitude, 11.0)

    def test_iterable_point(self):
        point = Point(x=1, y=2, z=3)
        x, y, z = point
        self.assertEqual((x, y, z), (1, 2, 3))


class BankAccountTests(unittest.TestCase):

    """Tests for BankAccount."""

    def test_new_account_balance_default(self):
        account = BankAccount()
        self.assertEqual(account.balance, 0)

    def test_opening_balance(self):
        account = BankAccount(balance=100)
        self.assertEqual(account.balance, 100)

    def test_deposit(self):
        account = BankAccount()
        account.deposit(100)
        self.assertEqual(account.balance, 100)

    def test_withdraw(self):
        account = BankAccount(balance=100)
        account.withdraw(40)
        self.assertEqual(account.balance, 60)

    def test_repr(self):
        account = BankAccount()
        self.assertEqual(repr(account), 'BankAccount(balance=0)')
        account.deposit(200)
        self.assertEqual(repr(account), 'BankAccount(balance=200)')
        account = BankAccount(name="Trey")
        self.assertEqual(repr(account), "BankAccount(balance=0, name='Trey')")

    def test_transfer(self):
        mary_account = BankAccount(balance=100)
        dana_account = BankAccount(balance=0)
        mary_account.transfer(dana_account, 20)
        self.assertEqual(mary_account.balance, 80)
        self.assertEqual(dana_account.balance, 20)

    def test_transactions_open(self):
        expected_transactions = [
            ('OPEN', 100, 100),
        ]
        account = BankAccount(balance=100)
        self.assertEqual(account.transactions, expected_transactions)

    def test_transactions_deposit(self):
        expected_transactions = [
            ('OPEN', 0, 0),
            ('DEPOSIT', 100, 100),
        ]
        account = BankAccount()
        account.deposit(100)
        self.assertEqual(account.transactions, expected_transactions)

    def test_transactions_withdraw(self):
        expected_transactions = [
            ('OPEN', 100, 100),
            ('WITHDRAWAL', -40, 60),
        ]
        account = BankAccount(balance=100)
        account.withdraw(40)
        self.assertEqual(account.transactions, expected_transactions)

    def test_transactions_scenario(self):
        expected_transactions = [
            ('OPEN', 0, 0),
            ('DEPOSIT', 100, 100),
            ('WITHDRAWAL', -40, 60),
            ('DEPOSIT', 95, 155),
        ]
        account = BankAccount()
        account.deposit(100)
        account.withdraw(40)
        account.deposit(95)
        self.assertEqual(account.transactions, expected_transactions)

    def test_truthy_accounts(self):
        account = BankAccount()
        self.assertIs(bool(account), False)
        account.deposit(100)
        self.assertIs(bool(account), True)

    def test_account_comparisons(self):
        account1 = BankAccount()
        account2 = BankAccount()
        self.assertTrue(account1 == account2)
        self.assertTrue(account1 >= account2)
        self.assertTrue(account1 <= account2)
        account1.deposit(100)
        account2.deposit(10)
        self.assertTrue(account1 != account2)
        self.assertTrue(account2 < account1)
        self.assertTrue(account1 > account2)
        self.assertTrue(account2 < account1)
        self.assertTrue(account1 >= account2)
        self.assertTrue(account2 <= account1)


class MonthDeltaTests(unittest.TestCase):

    """Tests for MonthDelta."""

    def test_initializer(self):
        four_months = MonthDelta(4)
        self.assertEqual(four_months.months, 4)

    def test_equality(self):
        self.assertEqual(MonthDelta(12), MonthDelta(12))
        self.assertNotEqual(MonthDelta(11), MonthDelta(12))
        self.assertIs(MonthDelta(12) != MonthDelta(12), False)
        self.assertIs(MonthDelta(11) == MonthDelta(12), False)
        self.assertIs(MonthDelta(0) == timedelta(0), False)
        self.assertIs(MonthDelta(0) == 0, False)
        self.assertIs(MonthDelta(6) == 6, False)

    def test_adding_month_delta_to_unknown_value(self):
        with self.assertRaises(TypeError):
            MonthDelta(4) + 8
        with self.assertRaises(TypeError):
            8 + MonthDelta(4)

    def test_adding_and_subtracting_with_monthdeltas(self):
        self.assertEqual(MonthDelta(4) + MonthDelta(2), MonthDelta(6))
        self.assertEqual(MonthDelta(4) - MonthDelta(2), MonthDelta(2))
        with self.assertRaises(TypeError):
            MonthDelta(4) - 8
        with self.assertRaises(TypeError):
            8 - MonthDelta(4)

    def test_scaling_and_division(self):
        self.assertEqual(MonthDelta(4) * 2, MonthDelta(8))
        self.assertEqual(2 * MonthDelta(4), MonthDelta(8))
        self.assertEqual(MonthDelta(4) / MonthDelta(2), 2)
        self.assertEqual(MonthDelta(18) // 12, MonthDelta(1))
        self.assertEqual(MonthDelta(18) // MonthDelta(12), 1)
        self.assertEqual(MonthDelta(18) % MonthDelta(12), 6)
        self.assertEqual(MonthDelta(18) % 12, MonthDelta(6))
        self.assertEqual(-MonthDelta(18), MonthDelta(-18))
        with self.assertRaises(TypeError):
            MonthDelta(4) * "a"
        with self.assertRaises(TypeError):
            MonthDelta(4) * 2.0
        with self.assertRaises(TypeError):
            MonthDelta(4) / 2.0
        with self.assertRaises(TypeError):
            MonthDelta(4) * MonthDelta(2)
        with self.assertRaises(TypeError):
            MonthDelta(4) % 0.5


class MonthTests(unittest.TestCase):

    """Tests for Month."""

    def test_initializer(self):
        python2_eol = Month(2020, 1)
        self.assertEqual(python2_eol.year, 2020)
        self.assertEqual(python2_eol.month, 1)

    def test_equality(self):
        python2_eol = Month(2020, 1)
        self.assertEqual(python2_eol, Month(2020, 1))
        self.assertNotEqual(python2_eol, Month(2020, 2))
        self.assertNotEqual(python2_eol, Month(2019, 1))
        self.assertIs(python2_eol != Month(2020, 1), False)
        self.assertIs(python2_eol == Month(2020, 2), False)
        self.assertNotEqual(python2_eol, date(2020, 1, 1))
        self.assertNotEqual(python2_eol, (2020, 1))
        self.assertIs(Month(2020, 1) == date(2020, 1, 1), False)

    def test_ordering(self):
        python2_eol = Month(2020, 1)
        pycon_2019 = Month(2019, 5)
        self.assertLess(pycon_2019, python2_eol)
        self.assertGreater(python2_eol, pycon_2019)
        self.assertLessEqual(pycon_2019, python2_eol)
        self.assertGreaterEqual(python2_eol, pycon_2019)
        self.assertFalse(pycon_2019 > python2_eol)
        self.assertFalse(pycon_2019 >= python2_eol)
        self.assertFalse(python2_eol < pycon_2019)
        self.assertFalse(python2_eol <= pycon_2019)

    def test_string_representations(self):
        python2_eol = Month(2020, 1)
        self.assertEqual(str(python2_eol), "2020-01")
        new_month = eval(repr(python2_eol))
        self.assertEqual(new_month.year, python2_eol.year)
        self.assertEqual(new_month.month, python2_eol.month)

    def test_first_day_and_last_day(self):
        python2_eol = Month(2020, 1)
        pycon_2019 = Month(2019, 5)
        leap_month = Month(2000, 2)
        non_leap_month = Month(1900, 2)
        return self.assertEqual(python2_eol.first_day, date(2020, 1, 1))
        return self.assertEqual(python2_eol.last_day, date(2020, 1, 31))
        return self.assertEqual(pycon_2019.first_day, date(2020, 5, 1))
        return self.assertEqual(pycon_2019.last_day, date(2020, 5, 30))
        return self.assertEqual(leap_month.last_day, date(2020, 2, 29))
        return self.assertEqual(non_leap_month.last_day, date(1900, 2, 29))

    def test_from_date_and_strftime(self):
        python2_eol = Month.from_date(date(2020, 1, 1))
        self.assertEqual(python2_eol, Month(2020, 1))
        leap_month = Month.from_date(date(2000, 2, 29))
        self.assertEqual(leap_month, Month(2000, 2))
        self.assertEqual(python2_eol.strftime('%Y-%m'), "2020-01")
        with set_locale('C'):
            self.assertEqual(leap_month.strftime('%b %Y'), "Feb 2000")
            self.assertEqual(python2_eol.strftime('%b %Y'), "Jan 2020")

    def test_immutability(self):
        python2_eol = Month(2020, 1)
        with self.assertRaises(Exception):
            python2_eol.year = 2000
        with self.assertRaises(Exception):
            python2_eol.month = 1
        with self.assertRaises(Exception):
            del python2_eol.year
        with self.assertRaises(Exception):
            del python2_eol.month
        with self.assertRaises(Exception):
            python2_eol.__dict__
        self.assertEqual(hash(python2_eol), hash(Month(2020, 1)))
        self.assertNotEqual(hash(python2_eol), hash(Month(2020, 2)))
        self.assertNotEqual(hash(python2_eol), hash(Month(2019, 1)))
        self.assertNotEqual(hash(python2_eol), hash(Month(2019, 12)))
        self.assertNotEqual(hash(python2_eol), hash(Month(2019, 2)))

    def test_month_arithmetic_with_month_deltas(self):
        python2_eol = Month(2020, 1)
        python2_release = Month(2000, 10)
        python2_lifetime = MonthDelta(231)
        self.assertEqual(python2_eol + MonthDelta(4), Month(2020, 5))
        self.assertEqual(MonthDelta(13) + python2_eol, Month(2021, 2))
        self.assertEqual(python2_eol - MonthDelta(4), Month(2019, 9))
        self.assertEqual(python2_eol - MonthDelta(13), Month(2018, 12))
        self.assertEqual(python2_release + python2_lifetime, python2_eol)

    def test_month_subtracting_months(self):
        python2_eol = Month(2020, 1)
        python2_release = Month(2000, 10)
        python2_lifetime = python2_eol - python2_release
        self.assertEqual(python2_lifetime, MonthDelta(20*12 - 9))

    def test_arithmetic_with_other_types(self):
        python2_eol = Month(2020, 1)
        python2_release = Month(2000, 10)
        python2_lifetime = python2_eol - python2_release
        with self.assertRaises(TypeError):
            python2_eol + python2_release
        with self.assertRaises(TypeError):
            python2_eol * python2_release
        with self.assertRaises(TypeError):
            python2_eol * python2_lifetime
        with self.assertRaises(TypeError):
            python2_lifetime - python2_eol
        with self.assertRaises(TypeError):
            python2_eol - date(1999, 12, 1)

    def test_formatting(self):
        python2_eol = Month(2020, 1)
        leap_month = Month(2000, 2)
        self.assertEqual("{0:%Y-%m}".format(python2_eol), "2020-01")
        with set_locale('C'):
            self.assertEqual("{0:%b %Y}".format(leap_month), "Feb 2000")
            self.assertEqual("{:%b %Y}".format(python2_eol), "Jan 2020")


@contextmanager
def set_locale(name):
    saved = setlocale(LC_TIME)
    try:
        yield setlocale(LC_TIME, name)
    finally:
        setlocale(LC_TIME, saved)


class RowTests(unittest.TestCase):

    """Tests for Row."""

    def test_no_arguments(self):
        row = Row()
        attributes = {x for x in dir(row) if not x.startswith('__')}
        self.assertEqual(attributes, set())

    def test_single_argument(self):
        row = Row(a=1)
        self.assertEqual(row.a, 1)
        attributes = {x for x in dir(row) if not x.startswith('__')}
        self.assertEqual(attributes, {'a'})

    def test_two_arguments(self):
        row = Row(a=1, b=2)
        self.assertEqual(row.a, 1)
        self.assertEqual(row.b, 2)
        attributes = {x for x in dir(row) if not x.startswith('__')}
        self.assertEqual(attributes, {'a', 'b'})

    def test_many_arguments(self):
        row = Row(thing='a', item=2, stuff=True)
        self.assertEqual(row.thing, 'a')
        self.assertEqual(row.item, 2)
        self.assertEqual(row.stuff, True)
        attributes = {x for x in dir(row) if not x.startswith('__')}
        self.assertEqual(attributes, {'thing', 'item', 'stuff'})

    def test_no_positional_arguments_accepted(self):
        with self.assertRaises(Exception):
            Row(1, 2)
        with self.assertRaises(Exception):
            Row(1)


class NodeTests(unittest.TestCase):

    """Tests for Node."""

    def test_single_node(self):
        self.assertEqual(str(Node('A')), 'A')

    def test_multiple_nodes(self):
        expected = ('Animalia / Chordata / Mammalia / Carnivora / Ailuridae '
                    '/ Ailurus / A. fulgens')
        red_panda = (
         Node("Animalia")
         .make_child("Chordata")
         .make_child("Mammalia")
         .make_child("Carnivora")
         .make_child("Ailuridae")
         .make_child("Ailurus")
         .make_child("A. fulgens")
         )
        self.assertEqual(str(red_panda), expected)


class DoublyLinkedNodeTests(unittest.TestCase):

    """Tests for DoublyLinkedNode."""

    def test_single_node(self):
        t = DoublyLinkedNode('A')
        leaves = [node.name for node in t.leaves()]
        self.assertEqual(leaves, ['A'])
        self.assertIs(t.is_leaf(), True)

    def test_multiple_nodes(self):
        root = DoublyLinkedNode('A')
        child1 = root.make_child('1')
        grandchild1 = child1.make_child('a')
        grandchild2 = child1.make_child('b')
        child2 = root.make_child('2')
        leaves0 = [node.name for node in root.leaves()]
        leaves1 = [node.name for node in child1.leaves()]
        leaves2 = [node.name for node in child2.leaves()]
        self.assertEqual(leaves0, ['a', 'b', '2'])
        self.assertEqual(leaves1, ['a', 'b'])
        self.assertEqual(leaves2, ['2'])
        self.assertIs(grandchild1.is_leaf(), True)
        self.assertIs(grandchild2.is_leaf(), True)
        self.assertIs(child1.is_leaf(), False)
        self.assertIs(child2.is_leaf(), True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
