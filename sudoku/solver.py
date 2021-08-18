"""
solver
"""

import pickle

from sudoku.exceptions import CustomException
from sudoku.grid import (
    get_cols_from_grid_rows,
    get_related_columns_for_index,
    get_square_from_position,
)
from sudoku.printer import pretty_printer


def _get_unique_candidate_in_grid_rows(grid_rows, row_index, sole_candidate):
    """
    get the unique candidate in grid state rows function
    :param row_index:
    :param sole_candidate:
    :return:
    """
    mapped_index = get_related_columns_for_index(row_index)
    if sole_candidate in (grid_rows[mapped_index[0]], grid_rows[mapped_index[1]]):
        return [sole_candidate]
    return None


def _get_unique_candidate_in_cols(grid_rows, col_index, sole_candidate):
    """
    get the unique candidate in columns function
    :param col_index:
    :param sole_candidate:
    :return:
    """
    mapped_index = get_related_columns_for_index(col_index)
    if sole_candidate in (
        get_cols_from_grid_rows(grid_rows)[mapped_index[0]],
        get_cols_from_grid_rows(grid_rows)[mapped_index[1]],
    ):
        return [sole_candidate]
    return None


def _get_solver_cell_candidates(grid_rows, row_index, col_index):
    """
    get solver cell candidates function
    :param grid_rows:
    :param row_index:
    :param col_index:
    :return:
    """
    square = get_square_from_position(grid_rows, row_index, col_index)
    sole_candidates = list(
        {1, 2, 3, 4, 5, 6, 7, 8, 9}
        - set(grid_rows[row_index])
        - set(square)
        - set(get_cols_from_grid_rows(grid_rows)[col_index])
    )
    for sole_candidate in sole_candidates:
        if _get_unique_candidate_in_grid_rows(grid_rows, row_index, sole_candidate):
            sole_candidates = (
                _get_unique_candidate_in_cols(grid_rows, col_index, sole_candidate)
                or sole_candidates
            )
            break
    return sole_candidates


def _deepcopy_grid_rows(grid_rows):
    """
    deepcopy rows with pickle loads dumps function
    :return:
    """
    return pickle.loads(pickle.dumps(grid_rows))


def _update_grid_rows_with_candidate(grid_rows, row_index, col_index, candidate):
    """
    update rows with candidate function
    :param row_index:
    :param col_index:
    :param candidate:
    :return:
    """
    grid_rows[row_index][col_index] = candidate
    return grid_rows


class Solver:
    """
    Solver class
    """

    def __init__(self, strategy):
        self.sudoku_solver_variations_queue = strategy

    def __str__(self):
        return str(self.sudoku_solver_variations_queue)

    def _put_rows_to_queue(self, grid_rows):
        """
        put rows to queue method
        :param grid_rows:
        :return:
        """
        self.sudoku_solver_variations_queue.put_nowait(grid_rows)

    def _grid_solver(self, grid_rows):
        """
        grid solver method
        :param grid_rows:
        :return:
        """
        for row_index, row in enumerate(grid_rows):
            for col_index in range(0, 9):
                if row[col_index] == 0:
                    candidates_left = _get_solver_cell_candidates(
                        grid_rows=grid_rows, row_index=row_index, col_index=col_index
                    )

                    if not candidates_left:
                        raise CustomException("NoCandidatesLeft")

                    if len(candidates_left) == 1:
                        row[col_index] = candidates_left[0]

                    else:
                        for candidate in candidates_left:
                            updated_rows = _update_grid_rows_with_candidate(
                                grid_rows=_deepcopy_grid_rows(grid_rows),
                                row_index=row_index,
                                col_index=col_index,
                                candidate=candidate,
                            )
                            self._put_rows_to_queue(updated_rows)

                        raise CustomException("TooManyCandidatesLeft")

        return grid_rows

    def sudoku_solver(self, prettify, initial_grid):
        """
        sudoku solver main method
        :param prettify:
        :param initial_grid:
        :return:
        """
        counter = 0
        self.sudoku_solver_variations_queue.put_nowait(initial_grid)
        while not self.sudoku_solver_variations_queue.empty():
            variation = self.sudoku_solver_variations_queue.get_nowait()
            counter += 1
            if counter > 10000000:
                raise CustomException("TooManyTries")

            try:
                sudoku_grid = self._grid_solver(
                    grid_rows=_deepcopy_grid_rows(variation)
                )
                for sudoku_row in sudoku_grid:
                    pretty_printer(prettify, sudoku_row)
                return counter
            # expected custom exception when no candidates left or
            # too many candidates left for the current state of the grid ->
            # continue processing queue items with the grid solver
            except CustomException:
                continue