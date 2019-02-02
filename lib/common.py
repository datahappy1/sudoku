import random

""" {square_index : [row_index range low : row_index range high], [col_index range low : col_index range high],...}"""
sq_to_row_col_map = {0: [[0, 3], [0, 3]], 1: [[0, 3], [3, 6]], 2: [[0, 3], [6, 9]],
                     3: [[3, 6], [0, 3]], 4: [[3, 6], [3, 6]], 5: [[3, 6], [6, 9]],
                     6: [[6, 9], [0, 3]], 7: [[6, 9], [3, 6]], 8: [[6, 9], [6, 9]]}


def sq_to_row_col_mapper(row_index, col_index):
    k, v = None, None
    for key, value in sq_to_row_col_map.items():
        if row_index in range(sq_to_row_col_map[key][0][0], sq_to_row_col_map[key][0][1]):
            if col_index in range(sq_to_row_col_map[key][1][0], sq_to_row_col_map[key][1][1]):
                k, v = key, value[1][0:2]
    return k, v


level_to_attempts_map = {'easy': 5000, 'medium': 50000, 'hard': 500000, 'default': 1000000}


def level_to_attempts_mapper(level):
    return level_to_attempts_map[level]


def get_random_subset_from_set(members_in, count_of_members_out):
    return random.sample(members_in, count_of_members_out)


def get_randint(range_start, range_end):
    return random.randint(range_start, range_end)
