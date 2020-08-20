"""Tests for pathlib exercises"""
from contextlib import contextmanager
from os import chdir, getcwd, listdir, mkdir
from os.path import basename, join
from tempfile import TemporaryDirectory
from textwrap import dedent
import unittest

from helpers import run_program, ModuleTestCase

from editorconfig import find_configs


@contextmanager
def cd(directory):
    old_dir = getcwd()
    chdir(directory)
    try:
        yield
    finally:
        chdir(old_dir)


class LSTests(ModuleTestCase):

    """
    Tests for ls.py

    List all files in a given directory
    """

    module_path = 'ls.py'

    def test_current_directory(self):
        with TemporaryDirectory() as tmp_dir:
            open(join(tmp_dir, 'file1.txt'), mode='wt').write('')
            open(join(tmp_dir, 'file2.txt'), mode='wt').write('hi')
            with cd(tmp_dir):
                output = run_program('ls.py')
        self.assertEqual(output, 'file1.txt\nfile2.txt\n')

    def test_different_directory(self):
        with TemporaryDirectory() as tmp_dir:
            open(join(tmp_dir, 'file1.txt'), mode='wt').write('')
            open(join(tmp_dir, 'file2.txt'), mode='wt').write('hi')
            output = run_program('ls.py', [tmp_dir])
        self.assertEqual(output, 'file1.txt\nfile2.txt\n')


class RemoveEmptyTests(ModuleTestCase):

    """
    Tests for remove_empty.py

    Remove all empty directories inside a given directory
    """

    module_path = 'remove_empty.py'

    def test_just_files(self):
        with TemporaryDirectory() as tmp_dir:
            open(join(tmp_dir, 'file1.txt'), mode='wt').write('')
            output = run_program('remove_empty.py', [tmp_dir])
            self.assertEqual(listdir(tmp_dir), ['file1.txt'])
        self.assertEqual(output, '')

    def test_no_empty_directories(self):
        with TemporaryDirectory() as tmp_dir:
            mkdir(join(tmp_dir, 'subdir1'))
            open(join(tmp_dir, 'subdir1', 'file1.txt'), mode='wt').write('')
            output = run_program('remove_empty.py', [tmp_dir])
            self.assertEqual(listdir(tmp_dir), ['subdir1'])
        self.assertEqual(output, '')

    def test_one_empty_directory(self):
        with TemporaryDirectory() as parent:
            tmp_dir = join(parent, 'tmp')
            dir1 = join(tmp_dir, 'subdir1')
            mkdir(tmp_dir)
            mkdir(dir1)
            output = run_program('remove_empty.py', [tmp_dir])
            with self.assertRaises(FileNotFoundError):
                listdir(tmp_dir)
            template = 'Deleting directory {}\nDeleting directory {}\n'
            self.assertEqual(
                output,
                template.format(dir1, tmp_dir),
            )

    def test_some_empty_directories(self):
        with TemporaryDirectory() as tmp_dir:
            dir1 = join(tmp_dir, 'subdir1')
            dir2 = join(tmp_dir, 'subdir2')
            dir3 = join(tmp_dir, 'subdir3')
            mkdir(dir1)
            mkdir(dir2)
            mkdir(dir3)
            open(join(dir2, 'file1.txt'), mode='wt').write('')
            output = run_program('remove_empty.py', [tmp_dir])
            self.assertEqual(listdir(tmp_dir), ['subdir2'])
        template = 'Deleting directory {}\nDeleting directory {}\n'
        self.assertIn(
            output,
            [template.format(dir1, dir3), template.format(dir3, dir1)]
        )

    def test_nested_empty_directories(self):
        with TemporaryDirectory() as tmp_dir:
            dir1 = join(tmp_dir, 'a')
            dir2 = join(tmp_dir, 'a', 'b')
            dir3 = join(tmp_dir, 'a', 'c')
            dir4 = join(tmp_dir, 'a', 'c', 'd')
            mkdir(dir1)
            mkdir(dir2)
            mkdir(dir3)
            mkdir(dir4)
            open(join(dir3, 'file1.txt'), mode='wt').write('')
            output = run_program('remove_empty.py', [tmp_dir])
            self.assertEqual(listdir(tmp_dir), ['a'])
            self.assertEqual(listdir(dir1), ['c'])
            self.assertEqual(listdir(dir3), ['file1.txt'])
        template = 'Deleting directory {}\nDeleting directory {}\n'
        self.assertIn(
            output,
            [template.format(dir2, dir4), template.format(dir4, dir2)]
        )


class EditorConfigTests(unittest.TestCase):

    """Tests for find_configs."""

    def test_nested_directories(self):
        with TemporaryDirectory() as tmp_dir:
            dir1 = join(tmp_dir, 'a')
            dir2 = join(tmp_dir, 'a', 'b')
            dir3 = join(tmp_dir, 'a', 'c')
            mkdir(dir1)
            mkdir(dir2)
            mkdir(dir3)
            fn1 = join(tmp_dir, '.editorconfig')
            fn2 = join(dir1, '.editorconfig')
            fn3 = join(dir3, '.editorconfig')
            open(fn1, mode='wt').write('1')
            open(fn2, mode='wt').write('2')
            open(fn3, mode='wt').write('3')
            configs = find_configs(join(dir2, 'hello.py'))
            self.assertEqual(configs, [(fn2, '2'), (fn1, '1')])

    def test_no_matches(self):
        with TemporaryDirectory() as tmp_dir:
            dir1 = join(tmp_dir, 'a')
            dir2 = join(tmp_dir, 'a', 'b')
            mkdir(dir1)
            mkdir(dir2)
            configs = find_configs(join(dir2, 'hello.py'))
            self.assertEqual(configs, [])


class TreeTests(ModuleTestCase):

    """
    Tests for tree.py

    Print tree structure of given directory and subdirectories.
    """

    module_path = 'tree.py'

    def test_current_directory(self):
        with TemporaryDirectory() as tmp_dir:
            dir1 = join(tmp_dir, 'a')
            dir2 = join(tmp_dir, 'a', 'b')
            dir3 = join(tmp_dir, 'a', 'c')
            mkdir(dir1)
            mkdir(dir2)
            mkdir(dir3)
            open(join(dir1, 'X.txt'), mode='wt').write('')
            open(join(dir3, 'Y.txt'), mode='wt').write('hi')
            with cd(tmp_dir):
                output = run_program('tree.py')
        self.assertEqual(output, dedent("""
            {}
            `-- a
                |-- X.txt
                |-- b
                `-- c
                    `-- Y.txt
        """.format(basename(tmp_dir))).lstrip())

    def test_different_directory(self):
        with TemporaryDirectory() as tmp_dir:
            dir1 = join(tmp_dir, 'a')
            dir2 = join(tmp_dir, 'a', 'b')
            dir3 = join(tmp_dir, 'a', 'c')
            mkdir(dir1)
            mkdir(dir2)
            mkdir(dir3)
            open(join(dir1, 'X.txt'), mode='wt').write('')
            open(join(dir3, 'Y.txt'), mode='wt').write('hi')
            with cd(tmp_dir):
                output = run_program('tree.py', ['a'])
        self.assertEqual(output, dedent("""
            a
            |-- X.txt
            |-- b
            `-- c
                `-- Y.txt
        """.format(basename(tmp_dir))).lstrip())


if __name__ == "__main__":
    unittest.main(verbosity=2)
