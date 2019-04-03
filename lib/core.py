"""
core.py
"""
from lib.common import get_random_subset_from_set, get_randint, sq_to_row_col_mapper, CustomException
import lib.gv as gv
import copy


class Core(object):
    """

    """
    def __init__(self, action, rows):
        """

        :param action:
        :param rows:
        """
        self.action = action
        self.rows = rows
        self.cols = []
        self.candidates_all = [candidate_index for candidate_index in range(1, 10)]
        self.squares = []

    def get_cell_unique_candidates(self, col_i, sole_cand, cands_left):
        # unique candidates in cols
        if col_i in (0, 3, 6):
            if sole_cand in (self.cols[col_i + 1]) and sole_cand in (self.cols[col_i + 2]):
                cands_left = [int(d) for d in str(sole_cand)]

        # unique candidates in cols
        if col_i in (1, 4, 7):
            if sole_cand in (self.cols[col_i + 1]) and sole_cand in (self.cols[col_i - 1]):
                cands_left = [int(d) for d in str(sole_cand)]

        # unique candidates in cols
        if col_i in (2, 5, 8):
            if sole_cand in (self.cols[col_i - 1]) and sole_cand in (self.cols[col_i - 2]):
                cands_left = [int(d) for d in str(sole_cand)]
        return cands_left

    def get_cell_candidates(self, row, row_index, col, col_index):
        """

        :param row:
        :param row_index:
        :param col:
        :param col_index:
        :return:
        """
        candidates_left = get_random_subset_from_set(self.candidates_all, 9)
        mapper_tuple = sq_to_row_col_mapper(row_index, col_index)
        square_index, slice1, slice2 = mapper_tuple[0], mapper_tuple[1][0], mapper_tuple[1][1]

        if self.action == 'generate':
            if row_index not in (0, 3, 6):
                mapper_tuple = sq_to_row_col_mapper(row_index, col_index)
                square_index, slice1, slice2 = mapper_tuple[0], mapper_tuple[1][0], mapper_tuple[1][1]
                self.squares[square_index].extend(self.rows[row_index - 1][slice(slice1, slice2)])
                candidates_left = list(set(candidates_left) - set(row) - set(self.squares[square_index]) -
                                       set(list(map(list, zip(*self.rows)))[col_index]))
            else:
                candidates_left = list(set(candidates_left) - set(row) - set(list(map(list, zip(*self.rows)))[col_index]))

            return candidates_left

        elif self.action == 'solve':
            self.cols[col_index] = list(map(list, zip(*self.rows)))[col_index]
            if row_index in (0, 3, 6):
                self.squares[square_index].extend(self.rows[row_index + 1][slice(slice1, slice2)])
                self.squares[square_index].extend(self.rows[row_index + 2][slice(slice1, slice2)])

                # sole candidates
                candidates_left = list(set(candidates_left) - set(row) - set(self.squares[square_index]) - set(col))

#                # unique candidates in rows
                for sole_candidate in candidates_left:
                    if sole_candidate in (self.rows[row_index + 1]) and sole_candidate in (self.rows[row_index + 2]):
                        # unique candidates in cols
                        candidates_left = Core.get_cell_unique_candidates(self, col_index, sole_candidate, candidates_left)

            if row_index in (1, 4, 7):
                self.squares[square_index].extend(self.rows[row_index - 1][slice(slice1, slice2)])
                self.squares[square_index].extend(self.rows[row_index + 1][slice(slice1, slice2)])

                # sole candidates
                candidates_left = list(set(candidates_left) - set(row) - set(self.squares[square_index]) -
                                       set(list(map(list, zip(*self.rows)))[col_index]))
                # unique candidates in rows
                for sole_candidate in candidates_left:
                    if sole_candidate in (self.rows[row_index - 1]) and sole_candidate in (self.rows[row_index + 1]):
                        # unique candidates in cols
                        candidates_left = Core.get_cell_unique_candidates(self, col_index, sole_candidate, candidates_left)

            if row_index in (2, 5, 8):
                self.squares[square_index].extend(self.rows[row_index - 1][slice(slice1, slice2)])
                self.squares[square_index].extend(self.rows[row_index - 2][slice(slice1, slice2)])

                # sole candidates
                candidates_left = list(set(candidates_left) - set(row) - set(self.squares[square_index]) -
                                       set(list(map(list, zip(*self.rows)))[col_index]))
                # unique candidates in rows
                for sole_candidate in candidates_left:
                    if sole_candidate in (self.rows[row_index - 1]) and sole_candidate in (self.rows[row_index - 2]):
                        # unique candidates in cols
                        candidates_left = Core.get_cell_unique_candidates(self, col_index, sole_candidate, candidates_left)

            return candidates_left

    def grid_solver(self):
        """

        :return:
        """
        self.squares = [[] for _ in range(9)]
        self.cols = list(map(list, zip(*self.rows)))

        for row_index, row in enumerate(self.rows):
            for col_index, col in enumerate(self.cols):
                if row[col_index] == 0:
                    cell = 0
                    candidates_left = Core.get_cell_candidates(self, row, row_index, col, col_index)
                    if len(candidates_left) == 0:
                        raise CustomException("NoCandidatesLeft")

                    if len(candidates_left) == 1:
                        cell = int(candidates_left[0])

                    if len(candidates_left) > 1:
                        for candidate in candidates_left:
                            rows = copy.deepcopy(self.rows)
                            rows[row_index][col_index] = candidate
                            if str(rows) not in gv.SUDOKU_VARIATIONS_AUX_SET:
                                gv.SUDOKU_VARIATIONS_AUX_SET.add(str(rows))
                                gv.SUDOKU_VARIATIONS_LIST.append(rows)
                        raise CustomException("TooManyCandidatesLeft")

                    row[col_index] = cell
                    self.cols = list(map(list, zip(*self.rows)))

        return self.rows

    def grid_generator(self):
        """

        :return:
        """
        row_index = 1
        self.rows.append(get_random_subset_from_set(self.candidates_all, 9))
        self.squares = [[] for _ in range(9)]
        while row_index < 9:
            row = []
            col_index = 0
            while col_index < 9:
                candidates_left = Core.get_cell_candidates(self, row, row_index, [], col_index)
                cell = int(get_random_subset_from_set(candidates_left, 1)[0]) if len(candidates_left) > 0 else -1
                if cell == -1:
                    raise ValueError
                row.append(cell)
                col_index = col_index + 1
            self.rows.append(row)
            row_index = row_index + 1
        return self.rows

    def row_mask(self, row, level):
        """

        :param row:
        :param level:
        :return:
        """
        if level == 'easy':
            hidden_members = get_random_subset_from_set(self.candidates_all, 3)
            for members in hidden_members:
                row[row.index(members)] = 0
        elif level == 'medium':
            count_of_hidden_members = get_randint(4, 5)
            hidden_members = get_random_subset_from_set(self.candidates_all, count_of_hidden_members)
            for members in hidden_members:
                row[row.index(members)] = 0
        elif level == 'hard':
            count_of_hidden_members = get_randint(5, 7)
            hidden_members = get_random_subset_from_set(self.candidates_all, count_of_hidden_members)
            salt = int(str(get_random_subset_from_set(self.candidates_all, 1)).strip('[]'))
            for members in hidden_members:
                row[row.index(members)] = 0
            if salt in row:
                row[row.index(salt)] = 0
        return row
