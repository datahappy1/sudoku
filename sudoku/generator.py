"""
generator
"""
from random import sample, randint
from typing import Set, List

from sudoku.exceptions import CustomException
from sudoku.grid import (
    get_col_from_grid_rows,
    get_square_from_position,
    ALL_CANDIDATES_SET,
)
from sudoku.level import Level
from sudoku.printer import pretty_printer


def _get_random_sample_from_set(
    set_of_input_members: Set[int], count_of_output_members: int
) -> List[int]:
    """
    get random sample from a set of integers function
    :param set_of_input_members:
    :param count_of_output_members:
    :return: list of random integers
    """
    return sample(tuple(set_of_input_members), count_of_output_members)


def _get_randint_from_range(range_start: int, range_end: int) -> int:
    """
    get random integer from a defined range function
    :param range_start:
    :param range_end:
    :return: random int
    """
    return randint(range_start, range_end)


def _add_row_mask(row: List[int], level: Level) -> List[int]:
    """
    add row mask function
    :param row:
    :param level:
    :return: row with hidden sudoku members
    """
    if level == Level.EASY:
        hidden_members = _get_random_sample_from_set(ALL_CANDIDATES_SET, 3)
        for members in hidden_members:
            row[row.index(members)] = 0

    elif level == Level.MEDIUM:
        count_of_hidden_members = _get_randint_from_range(4, 5)
        hidden_members = _get_random_sample_from_set(
            ALL_CANDIDATES_SET, count_of_hidden_members
        )

        for members in hidden_members:
            row[row.index(members)] = 0

    elif level == Level.HARD:
        count_of_hidden_members = _get_randint_from_range(5, 7)
        hidden_members = _get_random_sample_from_set(
            ALL_CANDIDATES_SET, count_of_hidden_members
        )

        extra_hidden_member = _get_random_sample_from_set(ALL_CANDIDATES_SET, 1)[0]

        for members in hidden_members:
            row[row.index(members)] = 0
        if extra_hidden_member in row:
            row[row.index(extra_hidden_member)] = 0

    return row


def _get_generator_cell_candidates(
    grid_rows: List[List[int]], candidate_row: List[int], row_index: int, col_index: int
) -> Set[int]:
    """
    get generator cell candidates function
    :param grid_rows:
    :param candidate_row:
    :param row_index:
    :param col_index:
    :return:
    """
    sole_candidates = (
        set(_get_random_sample_from_set(ALL_CANDIDATES_SET, 9))
        - set(candidate_row)
        - get_col_from_grid_rows(grid_rows, col_index)
    )

    if row_index in (1, 2, 4, 5, 7, 8):
        sole_candidates -= get_square_from_position(grid_rows, row_index, col_index)

    return sole_candidates


def _get_initial_grid_rows_with_first_random_row() -> List[List[int]]:
    """
    get initial grid state rows with first random row
    :return:
    """
    return [_get_random_sample_from_set(ALL_CANDIDATES_SET, 9)]


def _grid_generator(grid_rows: List[List[int]]):
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
            candidates_left = _get_generator_cell_candidates(
                grid_rows, candidate_row, row_index, col_index
            )

            cell = (
                _get_random_sample_from_set(candidates_left, 1)[0]
                if candidates_left
                else None
            )
            if not cell:
                raise CustomException("NoCandidatesLeft")
            candidate_row.append(cell)
            col_index += 1
        grid_rows.append(candidate_row)
        row_index += 1
    return grid_rows


def sudoku_generator(prettify: bool, level: str) -> int:
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
                masked_row = _add_row_mask(sudoku_row, level)
                pretty_printer(prettify, masked_row)
            return counter
        # expected custom exception when no candidates left for the current grid
        # restart grid generator
        except CustomException:
            continue
