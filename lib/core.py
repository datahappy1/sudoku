from lib.common import get_random_subset_from_set, get_randint, sq_to_row_col_mapper


class Core(object):
    """
    project main Core class
    """
    def __init__(self, squares, rows):
        """
        class Core __init__ function
        :param rows:
        """
        self.candidates_all = [candidate_index for candidate_index in range(1, 10)]
        self.squares = squares
        self.rows = rows
        self.cols = []

    def get_cell_candidates(self, row, row_index, col_index):
        """
        get cell candidates function
        :param row: grid row
        :param row_index: row index in the grid
        :param col_index: column index in the grid
        :return: possible candidates to fill a sudoku cell
        """
        candidates_left = get_random_subset_from_set(self.candidates_all, 9)
        if row_index not in (0, 3, 6):
            mapper_tuple = sq_to_row_col_mapper(row_index, col_index)
            square_index, slice1, slice2 = mapper_tuple[0], mapper_tuple[1][0], mapper_tuple[1][1]
            self.squares[square_index].extend(self.rows[row_index - 1][slice(slice1, slice2)])
            candidates_left = list(set(candidates_left) - set(row) - set(self.squares[square_index]) -
                                   set(list(map(list, zip(*self.rows)))[col_index]))
        else:
            candidates_left = list(set(candidates_left) - set(row) - set(list(map(list, zip(*self.rows)))[col_index]))
        return candidates_left

    def grid_solver(self):
        """
        sudoku grid generator function
        :return: grid filled with valid sudoku numbers
        """
        self.squares = [[] for _ in range(9)]
        self.cols = [[] for _ in range(9)]

        for row_index, row in enumerate(self.rows):
            for col_index, col in enumerate(self.cols):
                candidates_left = Core.get_cell_candidates(self, row, row_index, col_index)
                if row[col_index] == 0:
                    cell = 0
                    cell = int(get_random_subset_from_set(candidates_left, 1)[0]) if len(candidates_left) > 0 else -1
                    if cell == -1:
                        raise ValueError
                    else:
                        row[col_index] = cell
        return self.rows

    def grid_generator(self):
        """
        sudoku grid generator function
        :return: grid filled with valid sudoku numbers
        """
        row_index = 1
        self.rows.append(get_random_subset_from_set(self.candidates_all, 9))
        self.squares = [[] for _ in range(9)]
        while row_index < 9:
            row = []
            col_index = 0
            while col_index < 9:
                candidates_left = Core.get_cell_candidates(self, row, row_index, col_index)
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
        row mask function masking the filled outsudoku numbers rows with _
        :param row: input row with filled out sudoku numbers
        :param level: level easy or medium
        :return: masked sudoku row
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
