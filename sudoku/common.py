"""
common.py
"""
import random
import functools


class CustomException(Exception):
    """
    custom exceptions class
    """


# {square_index : [row_index range low : row_index range high], [col_index low : col_index high]}
SQ_TO_ROW_COL_MAP = {0: [[0, 3], [0, 3]], 1: [[0, 3], [3, 6]], 2: [[0, 3], [6, 9]],
                     3: [[3, 6], [0, 3]], 4: [[3, 6], [3, 6]], 5: [[3, 6], [6, 9]],
                     6: [[6, 9], [0, 3]], 7: [[6, 9], [3, 6]], 8: [[6, 9], [6, 9]]}

GENERIC_GRID_MAP = {0: [1, 2], 3: [4, 5], 6: [7, 8],
                    1: [2, 0], 4: [5, 3], 7: [8, 6],
                    2: [1, 0], 5: [4, 3], 8: [7, 6]}


@functools.lru_cache(128)
def sq_to_row_col_mapper(row_index, col_index):
    """
    grid square to row and col mapping function
    :param row_index:
    :param col_index:
    :return: key, value with mappings
    """
    k_out, v_out = None, None
    for key, value in SQ_TO_ROW_COL_MAP.items():
        if row_index in range(SQ_TO_ROW_COL_MAP[key][0][0], SQ_TO_ROW_COL_MAP[key][0][1]):
            if col_index in range(SQ_TO_ROW_COL_MAP[key][1][0], SQ_TO_ROW_COL_MAP[key][1][1]):
                k_out, v_out = key, value[1][0:2]
    return k_out, v_out


@functools.lru_cache(128)
def generic_grid_mapper(index):
    """
    grid offset mapping function
    this function takes column index or row index and returns
    the indexes affected in order to solve the grid
    :param index:
    :return: value with mappings
    """
    return [value for key, value in GENERIC_GRID_MAP.items() if key == index][0]


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
