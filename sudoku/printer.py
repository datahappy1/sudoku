"""
printer.py
"""


def pretty_printer(prettify, sudoku_row):
    """
    sudoku pretty printer function
    :param prettify:
    :param sudoku_row:
    :return: solved sudoku
    """
    if prettify is True:
        print(*sudoku_row)
    else:
        print(sudoku_row)
