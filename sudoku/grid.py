"""
grid
"""
import functools

from sudoku.randomness import get_random_sample_from_list, get_randint_from_range
from sudoku.level import Level

ALL_CANDIDATES_LIST = list(range(1, 10))


def get_cols_from_grid_rows(grid_rows):
    """
    get columns from grid represented in rows
    :param grid_rows:
    :return:
    """
    return list(map(list, zip(*grid_rows)))


@functools.lru_cache(128)
def get_related_columns_for_index(index):
    """
    grid offset mapping function
    this function takes column index or row index and returns
    the indexes affected in order to solve the grid
    :param index:
    :return: value with mappings
    """
    # {col_index:(related_col_index1, related_col_index2),} or
    # {row_index:(related_row_index1, related_row_index2),}
    generic_grid_map = {0: (1, 2), 1: (2, 0), 2: (1, 0),
                        3: (4, 5), 4: (5, 3), 5: (4, 3),
                        6: (7, 8), 7: (8, 6), 8: (7, 6)}

    return [value for key, value in generic_grid_map.items() if key == index][0]


@functools.lru_cache(128)
def _get_related_columns_from_square_for_position(row_index, col_index):
    """
    grid square to row and col mapping function
    :param row_index:
    :param col_index:
    :return: key, value with mappings
    """
    square_to_row_map = {0: (0, 3), 1: (0, 3), 2: (0, 3),
                         3: (3, 6), 4: (3, 6), 5: (3, 6),
                         6: (6, 9), 7: (6, 9), 8: (6, 9)}

    square_to_col_map = {0: (0, 3), 1: (3, 6), 2: (6, 9),
                         3: (0, 3), 4: (3, 6), 5: (6, 9),
                         6: (0, 3), 7: (3, 6), 8: (6, 9)}

    for key, value in square_to_col_map.items():
        if square_to_row_map[key][0] <= row_index < square_to_row_map[key][1] and \
                square_to_col_map[key][0] <= col_index < square_to_col_map[key][1]:
            return value
    return None


def get_square_from_position(grid_rows, row_index, col_index):
    """
    get square from position on grid
    :param grid_rows:
    :param row_index:
    :param col_index:
    :return:
    """
    square = []

    mapped_square_to_columns = _get_related_columns_from_square_for_position(row_index, col_index)
    row_sliced_from, row_sliced_to = (
        mapped_square_to_columns[0],
        mapped_square_to_columns[1]
    )

    try:
        square.extend(
            grid_rows[get_related_columns_for_index(row_index)[0]]
            [slice(row_sliced_from, row_sliced_to)]
        )
    except IndexError:
        pass
    try:
        square.extend(
            grid_rows[get_related_columns_for_index(row_index)[1]]
            [slice(row_sliced_from, row_sliced_to)]
        )
    except IndexError:
        pass

    return square


def add_row_mask(row, level):
    """
    add row mask function
    :param row:
    :param level:
    :return: row with hidden sudoku members
    """
    if level == Level.easy:
        hidden_members = get_random_sample_from_list(ALL_CANDIDATES_LIST, 3)
        for members in hidden_members:
            row[row.index(members)] = 0

    elif level == Level.medium:
        count_of_hidden_members = get_randint_from_range(4, 5)
        hidden_members = \
            get_random_sample_from_list(ALL_CANDIDATES_LIST, count_of_hidden_members)

        for members in hidden_members:
            row[row.index(members)] = 0

    elif level == Level.hard:
        count_of_hidden_members = get_randint_from_range(5, 7)
        hidden_members = \
            get_random_sample_from_list(ALL_CANDIDATES_LIST, count_of_hidden_members)

        extra_hidden_member = get_random_sample_from_list(ALL_CANDIDATES_LIST, 1)[0]

        for members in hidden_members:
            row[row.index(members)] = 0
        if extra_hidden_member in row:
            row[row.index(extra_hidden_member)] = 0

    return row
