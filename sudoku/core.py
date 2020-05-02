"""
core.py
"""
import pickle

from sudoku.common import get_random_subset_from_set, get_randint, \
    sq_to_row_col_mapper, generic_grid_mapper, CustomException
from sudoku import gv


class Core:
    """
    sudoku generator and solver worker class
    """
    def __init__(self, action):
        """
        init function
        :param action:
        :param rows:
        """
        self.action = action
        self.rows = []
        self.cols = []
        self.candidates_all = list(range(1, 10))
        self.squares = []

    def get_unique_candidate_in_cols(self, col_index, sole_candidate):
        """
        get the unique candidate in columns
        :param col_index:
        :param sole_candidate:
        :return:
        """
        mapped_index = generic_grid_mapper(col_index)
        if sole_candidate in self.cols[mapped_index[0]] \
                and sole_candidate in self.cols[mapped_index[1]]:
            return [sole_candidate]
        return None

    def get_cell_candidates(self, row, row_index, col, col_index):
        """
        get all possible cell candidates function
        :param row:
        :param row_index:
        :param col:
        :param col_index:
        :return:
        """
        candidates_left = None
        mapper_tuple = sq_to_row_col_mapper(row_index, col_index)
        square_index, slice1, slice2 = mapper_tuple[0], mapper_tuple[1][0], mapper_tuple[1][1]

        if self.action == "generate":
            candidates_left = set(get_random_subset_from_set(self.candidates_all, 9))
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

            mapped_index = generic_grid_mapper(row_index)

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
                        Core.get_unique_candidate_in_cols(self, col_index, sole_candidate) \
                        or candidates_left

        return candidates_left

    def multiple_candidates_handler(self, row_index, col_index, candidate):
        """
        multiple candidates handler function

        *2019/06/25 as a performance improvement, pickle was chosen over copy.deepcopy,
        to revert this, you need to import copy in this module and inside this function change
        rows = pickle.loads(pickle.dumps(self.rows, -1)) to rows = copy.deepcopy(self.rows)

        :param row_index:
        :param col_index:
        :param candidate:
        :return:
        """
        rows = pickle.loads(pickle.dumps(self.rows, -1))
        rows[row_index][col_index] = candidate
        gv.SUDOKU_VARIATIONS_QUEUE.put_nowait(rows)

    def grid_solver(self, rows):
        """
        grid solver function
        :return: all solved rows for sudoku grid
        """
        self.rows = rows
        self.squares = [[] for _ in range(9)]
        self.cols = list(map(list, zip(*self.rows)))

        for row_index, row in enumerate(self.rows):
            for col_index, col in enumerate(self.cols):
                if row[col_index] == 0:
                    candidates_left = \
                        Core.get_cell_candidates(self, row, row_index, col, col_index)

                    if not candidates_left:
                        raise CustomException("NoCandidatesLeft")

                    if len(candidates_left) == 1:
                        cell = candidates_left[0]

                    else:
                        for candidate in candidates_left:
                            Core.multiple_candidates_handler(self, row_index, col_index, candidate)
                        raise CustomException("TooManyCandidatesLeft")

                    row[col_index] = cell
                    self.cols = list(map(list, zip(*self.rows)))

        return self.rows

    def grid_generator(self, rows):
        """
        grid generator function
        :return: all rows for sudoku grid
        """
        self.rows = rows
        self.rows.append(get_random_subset_from_set(self.candidates_all, 9))
        self.squares = [[] for _ in range(9)]

        row_index = 1

        while row_index < 9:
            row = []
            col_index = 0
            while col_index < 9:
                candidates_left = Core.get_cell_candidates(self, row, row_index, [], col_index)
                cell = get_random_subset_from_set(candidates_left, 1)[0] if candidates_left \
                    else None

                if not cell:
                    raise CustomException("NoCandidatesLeft")

                row.append(cell)
                col_index += 1
            self.rows.append(row)
            row_index += 1

        return self.rows

    def row_mask(self, row, level):
        """
        row masking function
        :param row:
        :param level:
        :return: row with hidden sudoku members
        """
        if level == "easy":
            hidden_members = get_random_subset_from_set(self.candidates_all, 3)
            for members in hidden_members:
                row[row.index(members)] = 0

        elif level == "medium":
            count_of_hidden_members = get_randint(4, 5)
            hidden_members = \
                get_random_subset_from_set(self.candidates_all, count_of_hidden_members)

            for members in hidden_members:
                row[row.index(members)] = 0

        elif level == "hard":
            count_of_hidden_members = get_randint(5, 7)
            hidden_members = \
                get_random_subset_from_set(self.candidates_all, count_of_hidden_members)

            salt = int(str(get_random_subset_from_set(self.candidates_all, 1)).strip('[]'))
            for members in hidden_members:
                row[row.index(members)] = 0
            if salt in row:
                row[row.index(salt)] = 0

        return row
