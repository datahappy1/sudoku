"""
utils.py
"""
import random


ALL_CANDIDATES_LIST = list(range(1, 10))


def get_random_sample(list_of_input_members, count_of_output_members):
    """
    get random sample from a list of integers function
    :param list_of_input_members:
    :param count_of_output_members:
    :return: list of random integers
    """
    return random.sample(list_of_input_members, count_of_output_members)


def get_randint(range_start, range_end):
    """
    get random integer from a defined range function
    :param range_start:
    :param range_end:
    :return: random int
    """
    return random.randint(range_start, range_end)


def add_row_mask(row, level):
    """
    sudoku generator row masking function
    :param row:
    :param level:
    :return: row with hidden sudoku members
    """
    if level == "easy":
        hidden_members = get_random_sample(ALL_CANDIDATES_LIST, 3)
        for members in hidden_members:
            row[row.index(members)] = 0

    elif level == "medium":
        count_of_hidden_members = get_randint(4, 5)
        hidden_members = \
            get_random_sample(ALL_CANDIDATES_LIST, count_of_hidden_members)

        for members in hidden_members:
            row[row.index(members)] = 0

    elif level == "hard":
        count_of_hidden_members = get_randint(5, 7)
        hidden_members = \
            get_random_sample(ALL_CANDIDATES_LIST, count_of_hidden_members)

        extra_hidden_member = get_random_sample(ALL_CANDIDATES_LIST, 1)[0]

        for members in hidden_members:
            row[row.index(members)] = 0
        if extra_hidden_member in row:
            row[row.index(extra_hidden_member)] = 0

    return row


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
