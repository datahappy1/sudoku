"""
generator
"""
from sudoku.exceptions import CustomException
from sudoku.grid import get_cols_from_grid_rows, get_square_from_position, add_row_mask, \
    ALL_CANDIDATES_LIST
from sudoku.printer import pretty_printer
from sudoku.randomness import get_random_sample_from_list


def _get_generator_cell_candidates(grid_rows, candidate_row, row_index, col_index):
    """
    get generator cell candidates function
    :param grid_rows:
    :param candidate_row:
    :param row_index:
    :param col_index:
    :return:
    """
    square = get_square_from_position(grid_rows, row_index, col_index)
    sole_candidates = set(get_random_sample_from_list(ALL_CANDIDATES_LIST, 9))
    if row_index in (1, 2, 4, 5, 7, 8):
        sole_candidates = sole_candidates \
                          - set(candidate_row) \
                          - set(square) \
                          - set(get_cols_from_grid_rows(grid_rows)[col_index])

    elif row_index in (0, 3, 6):
        sole_candidates = sole_candidates \
                          - set(candidate_row) \
                          - set(get_cols_from_grid_rows(grid_rows)[col_index])
    return sole_candidates


def _get_initial_grid_rows_with_first_random_row():
    """
    get initial grid state rows with first random row
    :return:
    """
    return [get_random_sample_from_list(ALL_CANDIDATES_LIST, 9)]


def _grid_generator(grid_rows):
    """
    grid generator function
    :param grid_rows:
    :return:
    """
    row_index = 1
    while row_index < 9:
        candidate_row = []
        col_index = 0
        while col_index < 9:
            candidates_left = _get_generator_cell_candidates(grid_rows, candidate_row,
                                                             row_index, col_index)

            cell = get_random_sample_from_list(candidates_left, 1)[0] if candidates_left else None
            if not cell:
                raise CustomException("NoCandidatesLeft")
            candidate_row.append(cell)
            col_index += 1
        grid_rows.append(candidate_row)
        row_index += 1
    return grid_rows


def sudoku_generator(prettify, level):
    """
    sudoku generator main function
    :param prettify:
    :param level:
    :return:
    """
    counter = 0
    while True:
        counter += 1
        if counter > 10000000:
            raise CustomException("TooManyTries")

        try:
            initial_rows = _get_initial_grid_rows_with_first_random_row()
            sudoku_grid = _grid_generator(grid_rows=initial_rows)
            for sudoku_row in sudoku_grid:
                masked_row = add_row_mask(sudoku_row, level)
                pretty_printer(prettify, masked_row)
            return counter
        # expected custom exception when no candidates left for the current grid
        # restart grid generator
        except CustomException:
            continue
