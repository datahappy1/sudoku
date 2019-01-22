"""Python Sudoku"""
# TODO multiprocessing, solver calling Core,
# https://stackoverflow.com/questions/36962462/terminate-a-python-multiprocessing-program-once-a-one-of-its-workers-meets-a-cer
# bug with multiple members removal from squares for each col_index in the
# same group, docstrings, pylint, e2e test

import random
import multiprocessing


def get_random_subset_from_set(members_in, count_of_members_out):
    """
    get random numbers subset from a set of numbers
    :param members_in:
    :param count_of_members_out:
    :return: subset of random numbers
    """
    return random.sample(members_in, count_of_members_out)


class Core(object):
    """
    project main Core class
    """
    def __init__(self, squares, rows):
        """
        class Core __init__ function
        :param squares:
        :param rows:
        """
        self.candidates_all = [candidate_index for candidate_index in range(1, 10)]
        self.sq_to_col_range_map = {0: "0:3", 1: "3:6", 2: "6:9", 3: "0:3", 4: "3:6",
                                    5: "6:9", 6: "0:3", 7: "3:6", 8: "6:9"}
        self.squares = squares
        self.rows = rows

    def get_cell_candidates(self, row, row_index, col_index, square_index=None):
        """
        get cell candidates function
        :param row: grid row
        :param row_index: row index in the grid
        :param col_index: column index in the grid
        :param square_index: square index in the grid
        :return: possible candidates to fill a sudoku cell
        """
        candidates_left = get_random_subset_from_set(self.candidates_all, 9)
        if square_index is not None:
            s1, s2 = int(self.sq_to_col_range_map[square_index][0]), int(self.sq_to_col_range_map[square_index][2])
            self.squares[square_index].extend(self.rows[row_index - 1][slice(s1, s2)])
            candidates_left = list(set(candidates_left) - set(row) - set(self.squares[square_index]) -
                                   set(list(map(list, zip(*self.rows)))[col_index]))
        else:
            candidates_left = list(set(candidates_left) - set(row) - set(list(map(list, zip(*self.rows)))[col_index]))
        return candidates_left

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
                if row_index < 3:
                    if col_index < 3:
                        candidates_left = Core.get_cell_candidates(self, row, row_index, col_index, square_index=0)
                    elif 2 < col_index < 6:
                        candidates_left = Core.get_cell_candidates(self, row, row_index, col_index, square_index=1)
                    elif 5 < col_index < 9:
                        candidates_left = Core.get_cell_candidates(self, row, row_index, col_index, square_index=2)
                elif row_index == 3:
                    candidates_left = Core.get_cell_candidates(self, row, row_index, col_index)
                elif 3 < row_index < 6:
                    if col_index < 3:
                        candidates_left = Core.get_cell_candidates(self, row, row_index, col_index, square_index=3)
                    elif 2 < col_index < 6:
                        candidates_left = Core.get_cell_candidates(self, row, row_index, col_index, square_index=4)
                    elif 5 < col_index < 9:
                        candidates_left = Core.get_cell_candidates(self, row, row_index, col_index, square_index=5)
                elif row_index == 6:
                    candidates_left = Core.get_cell_candidates(self, row, row_index, col_index)
                elif 6 < row_index < 9:
                    if col_index < 3:
                        candidates_left = Core.get_cell_candidates(self, row, row_index, col_index, square_index=6)
                    elif 2 < col_index < 6:
                        candidates_left = Core.get_cell_candidates(self, row, row_index, col_index, square_index=7)
                    elif 5 < col_index < 9:
                        candidates_left = Core.get_cell_candidates(self, row, row_index, col_index, square_index=8)

                cell = int(get_random_subset_from_set(candidates_left, 1)[0]) if len(candidates_left) > 0 else 0

                if cell == 0:
                    return -1

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
                row[row.index(members)] = '_'
        elif level == 'medium':
            hidden_members = get_random_subset_from_set(self.candidates_all, 4)
            salt = int(str(get_random_subset_from_set(self.candidates_all, 1)).strip('[]'))
            for members in hidden_members:
                row[row.index(members)] = '_'
            if salt in row:
                row[row.index(salt)] = '_'
        return row


def __main__(level):
    """
    the project main function
    :param level: level easy or medium
    :return: final sudoku game
    """
    attempts = 0
    max_attempts = 5000
    while attempts <= max_attempts:
        try:
            obj = Core(squares=[], rows=[])
            sudoku_grid = Core.grid_generator(obj)
            for sudoku_row in sudoku_grid:
                #print(*sudoku_row)
                print(*Core.row_mask(obj, sudoku_row, level))
            attempts = attempts + 1
            break
        except TypeError:
            attempts = attempts + 1
            continue
        finally:
            if divmod(attempts, 1000)[1] == 1 and attempts > 1:
                print(f'attempts to generate a game: {str(attempts - 1)}')
    else:
        print(f'no game generated before reaching max attempts {max_attempts}')


if __name__ == '__main__':
    #__main__(level='easy')
    __main__(level='medium')
