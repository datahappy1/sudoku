import _thread
from lib.common import get_random_subset_from_set, get_randint, sq_to_row_col_mapper, get_random_subset_from_set_shuffle, CustomException


class Core(object):
    def __init__(self, action, rows):
        self.action = action
        self.rows = rows
        self.cols = []
        self.candidates_all = [candidate_index for candidate_index in range(1, 10)]
        self.squares = []

    def get_cell_candidates(self, row, row_index, col, col_index):
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
                                       #set(list(map(list, zip(*self.rows)))[col_index]))

                # unique candidates in rows
                for sole_candidate in candidates_left:
                    if sole_candidate in (self.rows[row_index + 1]) and sole_candidate in (self.rows[row_index + 2]):
                        # unique candidates in cols
                        if col_index in (0, 3, 6):
                            if sole_candidate in (self.cols[col_index + 1]) and sole_candidate in (self.cols[col_index + 2]):
                                candidates_left = [int(d) for d in str(sole_candidate)]

                        # unique candidates in cols
                        if col_index in (1, 4, 7):
                            if sole_candidate in (self.cols[col_index + 1]) and sole_candidate in (self.cols[col_index - 1]):
                                candidates_left = [int(d) for d in str(sole_candidate)]

                        # unique candidates in cols
                        if col_index in (2, 5, 8):
                            if sole_candidate in (self.cols[col_index - 1]) and sole_candidate in (self.cols[col_index - 2]):
                                candidates_left = [int(d) for d in str(sole_candidate)]

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
                        if col_index in (0, 3, 6):
                            if sole_candidate in (self.cols[col_index + 1]) and sole_candidate in (self.cols[col_index + 2]):
                                candidates_left = [int(d) for d in str(sole_candidate)]

                        # unique candidates in cols
                        if col_index in (1, 4, 7):
                            if sole_candidate in (self.cols[col_index + 1]) and sole_candidate in (self.cols[col_index - 1]):
                                candidates_left = [int(d) for d in str(sole_candidate)]

                        # unique candidates in cols
                        if col_index in (2, 5, 8):
                            if sole_candidate in (self.cols[col_index - 1]) and sole_candidate in (self.cols[col_index - 2]):
                                candidates_left = [int(d) for d in str(sole_candidate)]

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
                        if col_index in (0, 3, 6):
                            if sole_candidate in (self.cols[col_index + 1]) and sole_candidate in (self.cols[col_index + 2]):
                                candidates_left = [int(d) for d in str(sole_candidate)]

                        # unique candidates in cols
                        if col_index in (1, 4, 7):
                            if sole_candidate in (self.cols[col_index + 1]) and sole_candidate in (self.cols[col_index - 1]):
                                candidates_left = [int(d) for d in str(sole_candidate)]

                        # unique candidates in cols
                        if col_index in (2, 5, 8):
                            if sole_candidate in (self.cols[col_index - 1]) and sole_candidate in (self.cols[col_index - 2]):
                                candidates_left = [int(d) for d in str(sole_candidate)]

            return candidates_left

    def grid_solver(self):
        self.squares = [[] for _ in range(9)]
        #self.cols = [[] for _ in range(9)]
        self.cols = list(map(list, zip(*self.rows)))

        unknown_cell_index = 0

        for row_index, row in enumerate(self.rows):
            for col_index, col in enumerate(self.cols):
                if row[col_index] == 0:
                    cell = 0
                    unknown_cell_index = unknown_cell_index + 1
                    candidates_left = Core.get_cell_candidates(self, row, row_index, col, col_index)

                    if len(candidates_left) > 3 and unknown_cell_index > 1:
                        raise CustomException("TooMuchEntrophy")

                    get_random_subset_from_set_shuffle(candidates_left)

#                    for c in candidates_left:
#                    # TODO _thread.start_new_thread

                    #cell = int(get_random_subset_from_set(candidates_left, 1)[0]) if len(candidates_left) > 0 else -1
                    cell = int(candidates_left[0]) if len(candidates_left) > 0 else -1

                    if cell == -1:
                        #raise ValueError
                        raise CustomException("NoCandidatesLeft")

                    else:
                        row[col_index] = cell
                        self.cols = list(map(list, zip(*self.rows)))

        return self.rows

    def grid_generator(self):
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
