"""Class exercises"""
from calendar import monthrange
from datetime import date
from functools import total_ordering
from math import sqrt


class Point(object):

    """Three-dimensional point."""

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def magnitude(self):
        """Return the magnitude of the Point"""
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def __eq__(self, other):
        """Return True if our point is equal to the other point."""
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __ne__(self, other):
        """Return True if our point is equal to the other point."""
        return not self.__eq__(other)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __repr__(self):
        """Return dev-readable representation of Point."""
        return "Point(x={}, y={}, z={})".format(self.x, self.y, self.z)


class BankAccount(object):

    """Bank account including an account balance."""

    def __init__(self, balance=0, name=None):
        self.balance = balance
        self.name = name
        self.transactions = [("OPEN", balance, balance)]

    def __str__(self):
        if self.name is None:
            return "Account with balance of ${}".format(self.balance)
        return "Account {name!r} with balance of ${balance}".format(
            name=self.name,
            balance=self.balance,
        )

    def __repr__(self):
        if self.name is None:
            return "{class_name}(balance={balance})".format(
                class_name=self.__class__.__name__,
                balance=self.balance,
            )
        return "{class_name}(balance={balance}, name={name!r})".format(
            class_name=self.__class__.__name__,
            balance=self.balance,
            name=self.name,
        )

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(("DEPOSIT", amount, self.balance))

    def withdraw(self, amount):
        self.balance -= amount
        self.transactions.append(("WITHDRAWAL", -amount, self.balance))

    def transfer(self, other_account, amount):
        self.withdraw(amount)
        other_account.deposit(amount)

    def __nonzero__(self):
        return self.balance > 0

    __bool__ = __nonzero__

    def __eq__(self, rhs):
        return self.balance == rhs.balance

    def __ne__(self, rhs):
        return self.balance != rhs.balance

    def __lt__(self, rhs):
        return self.balance < rhs.balance

    def __gt__(self, rhs):
        return self.balance > rhs.balance

    def __le__(self, rhs):
        return self.balance <= rhs.balance

    def __ge__(self, rhs):
        return self.balance >= rhs.balance


@total_ordering
class MonthDelta(object):

    """Class representing a difference between months."""

    __slots__ = ['months']

    def __init__(self, months):
        super(MonthDelta, self).__setattr__('months', months)

    def __repr__(self):
        return "Month({})".format(self.months)

    def __eq__(self, other):
        if not isinstance(other, MonthDelta):
            return NotImplemented
        return self.months == other.months

    def __lt__(self, other):
        if not isinstance(other, MonthDelta):
            return NotImplemented
        return self.months < other.months

    def __setattr__(self, name, value):
        raise NotImplementedError

    def __delattr__(self, name):
        raise NotImplementedError

    def __hash__(self):
        return hash(self.months)

    def __add__(self, other):
        if isinstance(other, Month):
            months = other.year * 12 + other.month + self.months
            year, month = divmod(months-1, 12)
            return Month(year, month+1)
        if isinstance(other, MonthDelta):
            return MonthDelta(self.months + other.months)
        return NotImplemented

    __radd__ = __add__

    def __mul__(self, other):
        if isinstance(other, int):
            return MonthDelta(self.months * other)
        return NotImplemented

    __rmul__ = __mul__

    def __div__(self, other):
        if isinstance(other, int):
            return MonthDelta(self.months / other)
        if isinstance(other, MonthDelta):
            return self.months / other.months
        return NotImplemented

    __truediv__ = __div__

    def __floordiv__(self, other):
        if isinstance(other, int):
            return MonthDelta(int(self.months / other))
        if isinstance(other, MonthDelta):
            return int(self.months / other.months)
        return NotImplemented

    def __mod__(self, other):
        if isinstance(other, int):
            return MonthDelta(self.months % other)
        if isinstance(other, MonthDelta):
            return self.months % other.months
        return NotImplemented

    def __neg__(self):
        return MonthDelta(-self.months)

    def __sub__(self, other):
        if isinstance(other, MonthDelta):
            return MonthDelta(self.months - other.months)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, Month):
            months = other.year * 12 + other.month - self.months
            year, month = divmod(months-1, 12)
            return Month(year, month+1)
        return NotImplemented


@total_ordering
class Month(object):

    """Class representing an entire month."""

    __slots__ = ['year', 'month']

    def __init__(self, year, month):
        super(Month, self).__setattr__('year', year)
        super(Month, self).__setattr__('month', month)

    def __str__(self):
        return "{0}-{1:02}".format(self.year, self.month)

    def __repr__(self):
        return "Month({0}, {1})".format(self.year, self.month)

    def __eq__(self, other):
        if not isinstance(other, Month):
            return NotImplemented
        return (self.year, self.month) == (other.year, other.month)

    def __lt__(self, other):
        if not isinstance(other, Month):
            return NotImplemented
        return (self.year, self.month) < (other.year, other.month)

    def __setattr__(self, name, value):
        raise NotImplementedError

    def __delattr__(self, name):
        raise NotImplementedError

    def __hash__(self):
        return hash((self.year, self.month))

    @property
    def first_day(self):
        return date(self.year, self.month, 1)

    @property
    def last_day(self):
        weekday_of_first_date, last_date = monthrange(self.year, self.month)
        return date(self.year, self.month, last_date)

    @classmethod
    def from_date(cls, date_obj):
        return cls(date_obj.year, date_obj.month)

    def strftime(self, fmt):
        return self.first_day.strftime(fmt)

    def __sub__(self, other):
        if isinstance(other, Month):
            my_months = self.year*12 + self.month
            other_months = other.year*12 + other.month
            return MonthDelta(my_months - other_months)
        return NotImplemented

    def __format__(self, fmt):
        return self.first_day.__format__(fmt)


class Row(object):

    """Row class that stores all given arguments as attributes."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        attrs = ", ".join(
            "%s=%r" % (key, value)
            for key, value in self.__dict__.items()
        )
        return "{class_name}({attrs})".format(
            class_name=self.__class__.__name__,
            attrs=attrs,
        )


class Node:

    """Nodes for use in making hierarchies or trees."""

    def __init__(self, name, **kwargs):
        self.ancestors = list(kwargs.pop('ancestors', []))
        self.name = name
        object.__init__(self, **kwargs)

    def ancestors_and_self(self):
        """Return iterable with our ordered ancestors and our own node."""
        return self.ancestors + [self]

    def make_child(self, *args, **kwargs):
        """Create and return a child node of the current node."""
        kwargs['ancestors'] = self.ancestors_and_self()
        return self.__class__(*args, **kwargs)

    def __str__(self):
        """Return a slash-delimited ancestors hierarchy for this node."""
        return " / ".join([
            node.name
            for node in self.ancestors_and_self()
        ])

    def __repr__(self):
        return self.name


class DoublyLinkedNode(Node):

    """Class with Nodes that are doubly-linked"""

    def __init__(self, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)
        self.children = []

    def make_child(self, *args, **kwargs):
        """Create and return a child node of the current node."""
        node = Node.make_child(self, *args, **kwargs)
        self.children.append(node)
        return node

    def leaves(self):
        """Return all leaves of the current node and all descendent nodes."""
        if self.is_leaf():
            return [self]
        else:
            return [
                node
                for child in self.children
                for node in child.leaves()
            ]

    def is_leaf(self):
        """Return True if this node is a leaf (node which has no children)."""
        return not self.children
