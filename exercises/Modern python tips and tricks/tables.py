"""
Copyright 2007 Richard Harris

The software is licensed according to the terms of the
PSF (Python Software Foundation) license found here:
http://www.python.org/psf/license/

"""
from __future__ import print_function
from builtins import str
from builtins import zip
from builtins import map
from builtins import range
import string
from textwrap import wrap

MIN = 1
UNBIASED = 2

def display_table(rows,             # List of tuples of data
                  headings=[],      # Optional headings for columns
                  col_widths=[],    # Column widths
                  col_justs=[],     # Column justifications (str.ljust, etc)
                  screen_width=80,  # Width of terminal
                  col_spacer=2,     # Space between columns
                  fill_char=' ',    # Fill character
                  col_sep='=',      # Separator char
                  row_term='\n',    # row terminator (could be <br />)
                  norm_meth=MIN,    # Screen width normailization method
                  ):

    _col_justs = list(col_justs)
    _col_widths = list(col_widths)

    # String-ify everything
    rows = [tuple((str(col) for col in row)) for row in rows]

    # Compute appropriate col_widths if not given
    if not col_widths:
        if headings:
            _col_widths = [max(row) for row in (list(map(len, col))
                           for col in zip(headings, *rows))]
        else:
            _col_widths = [max(row) for row in (list(map(len, col))
                           for col in zip(*rows))]

    num_cols = len(_col_widths)
    col_spaces = col_spacer * (num_cols - 1)

    # Compute the size a row in our table would be in chars
    def _get_row_size(cw):
        return sum(cw) + col_spaces

    row_size = _get_row_size(_col_widths)

    def _unbiased_normalization():
        """ Normalize keeping the ratio of column sizes the same """
        __col_widths = [int(col_width *
                           (float(screen_width - col_spaces) / row_size))
                       for col_width in _col_widths]

        # Distribute epsilon underage to the the columns
        for x in range(screen_width - _get_row_size(__col_widths)):
            __col_widths[x % num_cols] += 1
        return __col_widths

    def _min_normalization():
        """ Bring all columns up to the minimum """
        __col_widths = _unbiased_normalization()

        # A made up heuristic -- hope it looks good
        col_min = int(0.5 * min(row_size, screen_width) / float(num_cols))

        # Bring all the columns up to the minimum
        norm_widths = []
        for col_width, org_width in zip(__col_widths, _col_widths):
            if col_width < col_min:
                col_width = min(org_width, col_min)
            norm_widths.append(col_width)

        # Distribute epsilon overage to the the columns
        count = _get_row_size(norm_widths) - screen_width
        x = 0
        while count > 0:
            if norm_widths[x % num_cols] > col_min:
                norm_widths[x % num_cols] -= 1
                count -= 1
            x += 1

        return norm_widths

    if not col_widths:
        # Normalize columns to screen size
        if row_size > screen_width:
            if norm_meth is UNBIASED:
                _col_widths = _unbiased_normalization()
            else:
                _col_widths = _min_normalization()

    row_size = _get_row_size(_col_widths)

    # If col_justs are not specified then guess the justification from
    # the appearence of the first row of data
    # Numbers and money are right justified, alpha beginning strings are left
    if not _col_justs:
        for col_datum in rows[0]:
            if isinstance(col_datum, str):
                if col_datum.startswith(tuple(string.digits + '$')):
                    _col_justs.append(str.rjust)
                else:
                    _col_justs.append(str.ljust)
            else:
                _col_justs.append(str.rjust)

    # Calculate the minimum screen width needed based on col_spacer and number
    # of columns
    min_screen_width = num_cols + col_spaces

    assert screen_width >= min_screen_width, "Screen Width is set too small, must be >= %d" % min_screen_width

    row_size = _get_row_size(_col_widths)

    def _display_wrapped_row(row, heading=False):
        """ Take a row, wrap it, and then display in proper tabular format
        """
        wrapped_row = [wrap(col_datum, col_width)
                        for col_datum, col_width in zip(row, _col_widths)]
        row_lines = []
        for cols in zip(*wrapped_row):
            if heading:
                partial = (str.center((partial_col or ''), col_width, fill_char)
                        for partial_col, col_width in zip(cols, _col_widths))
            else:
                partial = (col_just((partial_col or ''), col_width, fill_char)
                        for partial_col, col_width, col_just in zip(cols,
                                                                    _col_widths,
                                                                    _col_justs))
            row_lines.append((fill_char * col_spacer).join(partial))

        print(row_term.join(row_lines))

    if headings:
        # Print out the headings
        _display_wrapped_row(headings, heading=True)

        # Print separator
        print(col_sep * row_size)

    # Print out the rows of data
    for row in rows:
        _display_wrapped_row(row)


if __name__ == "__main__":
    import sys
    from io import StringIO
    old_stdout, sys.stdout = sys.stdout, StringIO()
    try:
        print("Demo 1")
        headings = ["Description", "Acct-Code", "Total"]
        rows = [("Catalytic Converter", "10-1000", "$100.23"),
                ("V-8, Fuel Injected, Hemispherically shaped head, custom valve springs, with a competition Torsion rotor", "10-1202", "$6300.00"),
                ("Power Clutch", "11-3440", "$330.32"),
                ("6-Speed Manual Transmission with paddle shifters, tungsten carbide syncronizers and dual-in-line throw-out bearings with reinforced steel armatures", "11-1000", "$3420.00")]
        display_table(rows, headings)

        print("\nDemo 2")
        rows = [(
        "Now is the time for all good men to come to the aid of their country. "*8,
        "This is a test of the emergency broadcast system. " * 5,
        "In Xanadu did Kublah Khan a pleasure dome decree. " * 7,
        )]
        display_table(rows)

        print("\nDemo 3")
        headings = ["Rank", "Movie Name"]
        rows = [(1, "Usual Suspects"), (2, "Memento"), (3, "There's Something About Mary"), (4, "Airplane"), (5, "The Godfather")]
        display_table(rows, headings)
    finally:
        sys.stdout, captured = old_stdout, sys.stdout
    expected = "Demo 1\n                        Description                          Acct-Code   Total  \n================================================================================\nCatalytic Converter                                            10-1000   $100.23\nV-8, Fuel Injected, Hemispherically shaped head, custom        10-1202  $6300.00\nPower Clutch                                                   11-3440   $330.32\n6-Speed Manual Transmission with paddle shifters, tungsten     11-1000  $3420.00\n\nDemo 2\nNow is the time for all good men to    This is a test of  In Xanadu did Kublah  \ncome to the aid of their country. Now  the emergency      Khan a pleasure dome  \nis the time for all good men to come   broadcast system.  decree. In Xanadu did \nto the aid of their country. Now is    This is a test of  Kublah Khan a pleasure\nthe time for all good men to come to   the emergency      dome decree. In Xanadu\nthe aid of their country. Now is the   broadcast system.  did Kublah Khan a     \ntime for all good men to come to the   This is a test of  pleasure dome decree. \naid of their country. Now is the time  the emergency      In Xanadu did Kublah  \nfor all good men to come to the aid    broadcast system.  Khan a pleasure dome  \nof their country. Now is the time for  This is a test of  decree. In Xanadu did \nall good men to come to the aid of     the emergency      Kublah Khan a pleasure\ntheir country. Now is the time for     broadcast system.  dome decree. In Xanadu\nall good men to come to the aid of     This is a test of  did Kublah Khan a     \ntheir country. Now is the time for     the emergency      pleasure dome decree. \nall good men to come to the aid of     broadcast system.  In Xanadu did Kublah  \n\nDemo 3\nRank           Movie Name         \n==================================\n   1  Usual Suspects              \n   2  Memento                     \n   3  There's Something About Mary\n   4  Airplane                    \n   5  The Godfather"
    if captured.getvalue().strip() != expected:
        print("\n\nExpected output:\n")
        print(expected)
        print("\n\nActual output:\n")
        print(captured.getvalue(), end='')
        print("\nError!\n")
    else:
        print("Output:\n")
        print(captured.getvalue(), end='')
        print("\nSuccess!\n")
