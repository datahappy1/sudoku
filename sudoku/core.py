"""
core.py
"""
import functools
import pickle
from enum import Enum

from sudoku.exceptions import CustomException
from sudoku.solver_strategy import SearchStrategyFactory, \
    BreadthFirstSearchStrategy, DepthFirstSearchStrategy
from sudoku.utils import get_random_sample, pretty_printer, add_row_mask, \
    ALL_CANDIDATES_LIST

DefaultSolverStrategy = [DepthFirstSearchStrategy, BreadthFirstSearchStrategy][0]


class ActionType(Enum):
    """
    ActionType enum class
    """
    solve = "solve"
    generate = "generate"


@functools.lru_cache(128)
def _get_related_columns(index):
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
def _get_square_with_related_columns(row_index, col_index):
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
            return key, value
    return None, None


class Core:
    """
    sudoku generator and solver worker class
    """

    def __init__(self, action):
        """
        init method
        :param action:
        """
        self.action = ActionType[action]
        self.rows = []
        self.cols = []
        self.squares = []

        self.sudoku_solver_variations_queue = \
            SearchStrategyFactory(DefaultSolverStrategy).get_strategy()

    def _get_unique_candidate_in_rows(self, row_index, sole_candidate):
        """
        get the unique candidate in rows method
        :param row_index:
        :param sole_candidate:
        :return:
        """
        mapped_index = _get_related_columns(row_index)
        if sole_candidate in self.rows[mapped_index[0]] \
                and sole_candidate in self.rows[mapped_index[1]]:
            return [sole_candidate]
        return None

    def _get_unique_candidate_in_cols(self, col_index, sole_candidate):
        """
        get the unique candidate in columns method
        :param col_index:
        :param sole_candidate:
        :return:
        """
        mapped_index = _get_related_columns(col_index)
        if sole_candidate in self.cols[mapped_index[0]] \
                and sole_candidate in self.cols[mapped_index[1]]:
            return [sole_candidate]
        return None

    def _get_cell_candidates(self, row, row_index, col, col_index):
        """
        get possible cell candidates method
        :param row:
        :param row_index:
        :param col:
        :param col_index:
        :return:
        """
        sole_candidates = None
        mapped_square_to_colums = _get_square_with_related_columns(row_index, col_index)
        square_index, row_sliced_from, row_sliced_to = mapped_square_to_colums[0], \
                                                       mapped_square_to_colums[1][0], \
                                                       mapped_square_to_colums[1][1]

        if self.action == ActionType.generate:
            sole_candidates = set(get_random_sample(ALL_CANDIDATES_LIST, 9))
            if row_index in (1, 2, 4, 5, 7, 8):
                self.squares[square_index].extend(
                    self.rows[row_index - 1][slice(row_sliced_from, row_sliced_to)]
                )
                sole_candidates = list(
                    sole_candidates - set(row) -
                    set(self.squares[square_index]) -
                    set(list(map(list, zip(*self.rows)))[col_index])
                )
            elif row_index in (0, 3, 6):
                sole_candidates = list(
                    sole_candidates - set(row) -
                    set(list(map(list, zip(*self.rows)))[col_index])
                )

        elif self.action == ActionType.solve:
            sole_candidates = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            self.cols[col_index] = list(map(list, zip(*self.rows)))[col_index]

            mapped_index = _get_related_columns(row_index)

            self.squares[square_index].extend(
                self.rows[mapped_index[0]][slice(row_sliced_from, row_sliced_to)]
            )
            self.squares[square_index].extend(
                self.rows[mapped_index[1]][slice(row_sliced_from, row_sliced_to)]
            )

            sole_candidates = list(
                sole_candidates - set(row) - set(self.squares[square_index]) - set(col)
            )

            for sole_candidate in sole_candidates:
                if self._get_unique_candidate_in_rows(row_index, sole_candidate):
                    sole_candidates = \
                        self._get_unique_candidate_in_cols(col_index, sole_candidate) \
                        or sole_candidates
                    break

        return sole_candidates

    def _deepcopy_rows(self):
        """
        deepcopy rows with pickle loads dumps method
        :return:
        """
        return pickle.loads(pickle.dumps(self.rows))

    @staticmethod
    def _update_rows_with_candidate(rows, row_index, col_index, candidate):
        """
        update rows with candidate
        :param row_index:
        :param col_index:
        :param candidate:
        :return:
        """
        rows[row_index][col_index] = candidate
        return rows

    def _put_rows_to_queue(self, rows):
        """
        put rows to queue
        :param rows:
        :return:
        """
        self.sudoku_solver_variations_queue.put_nowait(rows)

    def _grid_solver(self, rows):
        """
        grid solver method
        :return: all solved rows for sudoku grid
        """
        self.rows = rows
        self.squares = [[] for _ in range(9)]
        self.cols = list(map(list, zip(*self.rows)))

        for row_index, row in enumerate(self.rows):
            for col_index, col in enumerate(self.cols):
                if row[col_index] == 0:
                    candidates_left = \
                        self._get_cell_candidates(row, row_index, col, col_index)

                    if not candidates_left:
                        raise CustomException("NoCandidatesLeft")

                    if len(candidates_left) == 1:
                        row[col_index] = candidates_left[0]
                        self.cols = list(map(list, zip(*self.rows)))

                    else:
                        for candidate in candidates_left:
                            updated_rows = self._update_rows_with_candidate(
                                self._deepcopy_rows(), row_index, col_index, candidate)
                            self._put_rows_to_queue(updated_rows)

                        raise CustomException("TooManyCandidatesLeft")

        return self.rows

    def _grid_generator(self, rows):
        """
        grid generator method
        :return: all rows for sudoku grid
        """
        self.rows = rows
        self.rows.append(get_random_sample(ALL_CANDIDATES_LIST, 9))
        self.squares = [[] for _ in range(9)]

        row_index = 1

        while row_index < 9:
            row = []
            col_index = 0
            while col_index < 9:
                candidates_left = self._get_cell_candidates(row, row_index, [], col_index)
                cell = get_random_sample(candidates_left, 1)[0] if candidates_left \
                    else None

                if not cell:
                    raise CustomException("NoCandidatesLeft")

                row.append(cell)
                col_index += 1
            self.rows.append(row)
            row_index += 1

        return self.rows

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
                sudoku_grid = self._grid_solver(rows=variation)
                for sudoku_row in sudoku_grid:
                    pretty_printer(prettify, sudoku_row)
                return counter
            # expected custom exception when no candidates left or
            # too many candidates left for the current state of the grid ->
            # continue processing queue items with the grid solver
            except CustomException:
                continue

    def sudoku_generator(self, prettify, level):
        """
        sudoku generator main method
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
                sudoku_grid = self._grid_generator(rows=[])
                for sudoku_row in sudoku_grid:
                    masked_row = add_row_mask(sudoku_row, level)
                    pretty_printer(prettify, masked_row)
                return counter
            # expected custom exception when no candidates left for the current grid
            # restart grid generator
            except CustomException:
                continue
