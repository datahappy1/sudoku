"""
common.py
"""
import random


class CustomException(Exception):
    """
    custom exceptions class
    """
    pass


""" {square_index : [row_index range low : row_index range high], [col_index range low : col_index range high],...}"""
sq_to_row_col_map = {0: [[0, 3], [0, 3]], 1: [[0, 3], [3, 6]], 2: [[0, 3], [6, 9]],
                     3: [[3, 6], [0, 3]], 4: [[3, 6], [3, 6]], 5: [[3, 6], [6, 9]],
                     6: [[6, 9], [0, 3]], 7: [[6, 9], [3, 6]], 8: [[6, 9], [6, 9]]}


def sq_to_row_col_mapper(row_index, col_index):
    """
    grid square to row and col mapping function
    :param row_index:
    :param col_index:
    :return: key, value with mappings
    """
    k, v = None, None
    for key, value in sq_to_row_col_map.items():
        if row_index in range(sq_to_row_col_map[key][0][0], sq_to_row_col_map[key][0][1]):
            if col_index in range(sq_to_row_col_map[key][1][0], sq_to_row_col_map[key][1][1]):
                k, v = key, value[1][0:2]
    return k, v


def get_random_subset_from_set(members_in, count_of_members_out):
    """
    get random subset of integers from a set of integers
    :param members_in:
    :param count_of_members_out:
    :return: list or random integers
    """
    return random.sample(members_in, count_of_members_out)


def get_randint(range_start, range_end):
    """
    get random integer from a defined range
    :param range_start:
    :param range_end:
    :return: random int
    """
    return random.randint(range_start, range_end)


def pretty_printer(prettify, sudoku_row):
    """
    final sudoku pretty printer function
    :param prettify:
    :param sudoku_row:
    :return: solved (prettified) sudoku
    """
    if prettify is True:
        print(*sudoku_row)
    else:
        print(sudoku_row)

