"""
core.py
"""
import pickle
import functools
from queue import LifoQueue
from sudoku.exceptions import CustomException
from sudoku.utils import get_random_subset_from_set, pretty_printer, add_row_mask, \
    ALL_CANDIDATES_LIST


class Core:
    """
    sudoku generator and solver worker class
    """

    def __init__(self, action):
        """
        init method
        :param action:
        """
        self.action = action
        self.rows = []
        self.cols = []
        self.squares = []
        self.generic_grid_map = {0: [1, 2], 1: [2, 0], 2: [1, 0],
                                 3: [4, 5], 4: [5, 3], 5: [4, 3],
                                 6: [7, 8], 7: [8, 6], 8: [7, 6]}
        # {square_index:[row_index range low:row_index range high],[col_index low:col_index high]}
        self.sq_to_row_col_map = {0: [[0, 3], [0, 3]], 1: [[0, 3], [3, 6]], 2: [[0, 3], [6, 9]],
                                  3: [[3, 6], [0, 3]], 4: [[3, 6], [3, 6]], 5: [[3, 6], [6, 9]],
                                  6: [[6, 9], [0, 3]], 7: [[6, 9], [3, 6]], 8: [[6, 9], [6, 9]]}
        self.sudoku_solver_variations_queue = LifoQueue()

    @functools.lru_cache(128)
    def _sq_to_row_col_mapper(self, row_index, col_index):
        """
        grid square to row and col mapping function
        :param row_index:
        :param col_index:
        :return: key, value with mappings
        """
        k_out, v_out = None, None
        for key, value in self.sq_to_row_col_map.items():
            if row_index in range(self.sq_to_row_col_map[key][0][0],
                                  self.sq_to_row_col_map[key][0][1]):
                if col_index in range(self.sq_to_row_col_map[key][1][0],
                                      self.sq_to_row_col_map[key][1][1]):
                    k_out, v_out = key, value[1][0:2]
                    break
        return k_out, v_out

    @functools.lru_cache(128)
    def _generic_grid_mapper(self, index):
        """
        grid offset mapping function
        this function takes column index or row index and returns
        the indexes affected in order to solve the grid
        :param index:
        :return: value with mappings
        """
        return [value for key, value in self.generic_grid_map.items() if key == index][0]

    def _get_unique_candidate_in_cols(self, col_index, sole_candidate):
        """
        get the unique candidate in columns method
        :param col_index:
        :param sole_candidate:
        :return:
        """
        mapped_index = self._generic_grid_mapper(col_index)
        if sole_candidate in self.cols[mapped_index[0]] \
                and sole_candidate in self.cols[mapped_index[1]]:
            return [sole_candidate]
        return None

    def _get_cell_candidates(self, row, row_index, col, col_index):
        """
        get all possible cell candidates method
        :param row:
        :param row_index:
        :param col:
        :param col_index:
        :return:
        """
        candidates_left = None
        mapper_tuple = self._sq_to_row_col_mapper(row_index, col_index)
        square_index, slice1, slice2 = mapper_tuple[0], mapper_tuple[1][0], mapper_tuple[1][1]

        if self.action == "generate":
            candidates_left = set(get_random_subset_from_set(ALL_CANDIDATES_LIST, 9))
            if row_index not in (0, 3, 6):
                self.squares[square_index].extend(self.rows[row_index - 1][slice(slice1, slice2)])
                candidates_left = list(candidates_left - set(row) -
                                       set(self.squares[square_index]) -
                                       set(list(map(list, zip(*self.rows)))[col_index]))

            else:
                candidates_left = list(candidates_left - set(row) -
                                       set(list(map(list, zip(*self.rows)))[col_index]))

        elif self.action == "solve":
            candidates_left = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            self.cols[col_index] = list(map(list, zip(*self.rows)))[col_index]

            mapped_index = self._generic_grid_mapper(row_index)

            self.squares[square_index].extend(self.rows[mapped_index[0]][slice(slice1, slice2)])
            self.squares[square_index].extend(self.rows[mapped_index[1]][slice(slice1, slice2)])

            # sole candidates
            candidates_left = list(candidates_left - set(row) -
                                   set(self.squares[square_index]) - set(col))

            # unique candidates in rows
            for sole_candidate in candidates_left:
                if sole_candidate in self.rows[mapped_index[0]] and \
                        sole_candidate in self.rows[mapped_index[1]]:
                    # unique candidates in cols
                    candidates_left = \
                        self._get_unique_candidate_in_cols(col_index, sole_candidate) \
                        or candidates_left
                    break
        return candidates_left

    def _multiple_candidates_handler(self, row_index, col_index, candidate):
        """
        multiple candidates handler method

        *2019/06/25 as a performance improvement, pickle was chosen over copy.deepcopy,
        to revert this, you need to import copy in this module and inside this method change
        rows = pickle.loads(pickle.dumps(self.rows, -1)) to rows = copy.deepcopy(self.rows)

        :param row_index:
        :param col_index:
        :param candidate:
        :return:
        """
        rows = pickle.loads(pickle.dumps(self.rows, -1))
        rows[row_index][col_index] = candidate
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
                            self._multiple_candidates_handler(row_index, col_index, candidate)
                        raise CustomException("TooManyCandidatesLeft")

        return self.rows

    def _grid_generator(self, rows):
        """
        grid generator method
        :return: all rows for sudoku grid
        """
        self.rows = rows
        self.rows.append(get_random_subset_from_set(ALL_CANDIDATES_LIST, 9))
        self.squares = [[] for _ in range(9)]

        row_index = 1

        while row_index < 9:
            row = []
            col_index = 0
            while col_index < 9:
                candidates_left = self._get_cell_candidates(row, row_index, [], col_index)
                cell = get_random_subset_from_set(candidates_left, 1)[0] if candidates_left \
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
