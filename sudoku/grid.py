"""
grid
"""

ALL_CANDIDATES_LIST = list(range(1, 10))


def get_col_from_grid_rows(grid_rows, col_index):
    """
    get column from grid represented in rows
    :param grid_rows:
    :param col_index:
    :return:
    """
    return list(map(list, zip(*grid_rows)))[col_index]


def _get_related_rows_for_row_index(index):
    """
    grid offset mapping function
    this function takes row index and returns
    the related rows
    :param index:
    :return: related_row_index1, related_row_index2
    """
    # {row_index:(related_row_index1, related_row_index2),}
    generic_grid_map = {
        0: (1, 2), 1: (2, 0), 2: (1, 0),
        3: (4, 5), 4: (5, 3), 5: (4, 3),
        6: (7, 8), 7: (8, 6), 8: (7, 6),
    }
    return generic_grid_map[index]


def get_square_from_position(grid_rows, row_index, col_index):
    """
    get square from position on grid
    :param grid_rows:
    :param row_index:
    :param col_index:
    :return:
    """
    square = []
    square_column_boundaries = None, None

    if col_index // 3 == 0:
        square_column_boundaries = 0, 3
    elif col_index // 3 == 1:
        square_column_boundaries = 3, 6
    elif col_index // 3 == 2:
        square_column_boundaries = 6, 9

    try:
        square.extend(
            grid_rows[_get_related_rows_for_row_index(row_index)[0]][
                slice(square_column_boundaries[0], square_column_boundaries[1])
            ]
        )
    except IndexError:
        # this is expected when generating grid, index error is raised for square
        # data lookups that are targeting rows/columns that haven't been yet populated
        pass
    try:
        square.extend(
            grid_rows[_get_related_rows_for_row_index(row_index)[1]][
                slice(square_column_boundaries[0], square_column_boundaries[1])
            ]
        )
    except IndexError:
        # this is expected when generating grid, index error is raised for square
        # data lookups that are targeting rows/columns that haven't been yet populated
        pass

    return square
