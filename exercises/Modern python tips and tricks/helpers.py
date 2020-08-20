"""Test helpers"""
from contextlib import contextmanager, redirect_stdout
from tempfile import NamedTemporaryFile
import os
import os.path
from io import StringIO
import imp
import sys
import unittest


class Mock:
    def __init__(self, side_effect=None):
        self.side_effect = side_effect
        self.calls = []
    def __call__(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        if callable(self.side_effect):
            return self.side_effect(*args, **kwargs)
        elif isinstance(self.side_effect, BaseException):
            raise self.side_effect
        elif self.side_effect is not None:
            return self.side_effect[len(self.calls)-1]
    def assert_not_called(self, *args, **kwargs):
        """This was not called."""
        assert self.calls == []
    def assert_called_once_with(self, *args, **kwargs):
        """This was called, exactly once, with the given arguments."""
        assert self.calls.count((args, kwargs)) == 1
    def assert_called_with(self, *args, **kwargs):
        """Last call to this function was with the given arguments."""
        assert self.calls[-1] == (args, kwargs)
    def assert_any_call(self, *args, **kwargs):
        """This was called at least once with the given arguments."""
        assert (args, kwargs) in self.calls


class DummyException(BaseException):
    """This should never be raised."""


def run_program(program, args=[], raises=DummyException):
    old_args = sys.argv
    assert all(isinstance(a, str) for a in args)
    try:
        path = os.path.join(os.path.dirname(__file__), program)
        sys.argv = [program] + args
        with redirect_stdout(StringIO()) as output:
            try:
                if '__main__' in sys.modules:
                    del sys.modules['__main__']
                imp.load_source('__main__', path)
            except raises:
                return output.getvalue()
            except SystemExit as e:
                if e.args != (0,):
                    raise
            if raises is not DummyException:
                raise AssertionError("{} not raised".format(raises))
            return output.getvalue()
    finally:
        sys.argv = old_args


def import_module(module, args=[]):
    path = 'modules/{module}.py'.format(module=module)
    return imp.load_source(module, path)


@contextmanager
def make_file(contents=None):
    with NamedTemporaryFile(mode='wt', delete=False) as f:
        if contents:
            f.write(contents)
    try:
        yield f.name
    finally:
        os.remove(f.name)


class ModuleTestCase(unittest.TestCase):

    """TestCase for module/program tests."""

    @classmethod
    def setUpClass(cls):
        if not hasattr(cls, 'module_path'):
            raise NotImplementedError('Test needs "module_path" attribute')
