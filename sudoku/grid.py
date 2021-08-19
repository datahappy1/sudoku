"""
grid
"""

ALL_CANDIDATES_LIST = list(range(1, 10))


def get_cols_from_grid_rows(grid_rows):
    """
    get columns from grid represented in rows
    :param grid_rows:
    :return:
    """
    return list(map(list, zip(*grid_rows)))


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

    def _get_related_columns_from_square_for_column_index():
        """
        get related columns from square for column index
        :return: lower and upper bound column indexes
        """
        if 0 <= col_index < 3:
            return 0, 3
        if 3 <= col_index < 6:
            return 3, 6
        if 6 <= col_index < 9:
            return 6, 9
        return None

    square = []

    mapped_square_to_columns = _get_related_columns_from_square_for_column_index()

    try:
        square.extend(
            grid_rows[get_related_columns_for_index(row_index)[0]][
                slice(mapped_square_to_columns[0], mapped_square_to_columns[1])
            ]
        )
    except IndexError:
        # this is expected when generating grid, index error is raised for square
        # data lookups that are targeting rows/columns that haven't been yet populated
        pass
    try:
        square.extend(
            grid_rows[get_related_columns_for_index(row_index)[1]][
                slice(mapped_square_to_columns[0], mapped_square_to_columns[1])
            ]
        )
    except IndexError:
        # this is expected when generating grid, index error is raised for square
        # data lookups that are targeting rows/columns that haven't been yet populated
        pass

    return square
