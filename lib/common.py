import random

""" {square_index : [row_index range low : row_index range high], [col_index range low : col_index range high],...}"""
sq_to_row_col_map = {0: [[1, 3], [0, 3]], 1: [[1, 3], [3, 6]], 2: [[1, 3], [6, 9]],
                     3: [[4, 6], [0, 3]], 4: [[4, 6], [3, 6]], 5: [[4, 6], [6, 9]],
                     6: [[7, 9], [0, 3]], 7: [[7, 9], [3, 6]], 8: [[7, 9], [6, 9]]}


def sq_to_row_col_mapper(row_index, col_index):
    """
    get square index if row index and col index provided
    :param row_index:
    :param col_index:
    :return: (square index, [col_index range low, col_index range high])
    """
    k, v = None, None
    for key, value in sq_to_row_col_map.items():
        if row_index in range(sq_to_row_col_map[key][0][0], sq_to_row_col_map[key][0][1]):
            if col_index in range(sq_to_row_col_map[key][1][0], sq_to_row_col_map[key][1][1]):
                k, v = key, value[1][0:2]
    return k, v


level_to_attempts_map = {'easy': 50, 'medium': 1000, 'hard': 50000, 'default': 50000}


def level_to_attempts_mapper(level):
    """
    get count of attempts based on the provided level
    :param level:
    :return:
    """
    attempts = level_to_attempts_map[level]
    return attempts


def get_random_subset_from_set(members_in, count_of_members_out):
    """
    get pseudo random numbers subset from a set of numbers
    :param members_in:
    :param count_of_members_out:
    :return: subset of random numbers
    """
    return random.sample(members_in, count_of_members_out)


def get_randint(range_start, range_end):
    """
    get a pseudo random integer N from range, a <= N <= b
    :param range_start:
    :param range_end:
    :return:
    """
    return random.randint(range_start, range_end)
