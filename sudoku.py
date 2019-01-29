import copy
from lib import core as core, common as common
from settings import beautify as default_beautify


def solver(rows_in, beautify=default_beautify):
    """
    the project main solver function
    :param rows_in: consuming list of lists with the sudoku to solve
    :param beautify: default from settings.py
    :return: final solved sudoku
    """
    attempts = 0
    max_attempts = common.level_to_attempts_mapper(level='default')
    rows_ref = copy.deepcopy(rows_in)
    while attempts <= max_attempts:
        try:
            obj = core.Core(rows=rows_ref)
            sudoku_grid = core.Core.grid_solver(obj)
            for sudoku_row in sudoku_grid:
                if bool(beautify):
                    print(*sudoku_row)
                else:
                    print(sudoku_row)
            attempts = attempts + 1
            print(attempts)
            break
        except ValueError:
            attempts = attempts + 1
            rows_ref = copy.deepcopy(rows_in)
            continue
        finally:
            if divmod(attempts, 100000)[1] == 1 and attempts > 1:
                print(f'attempts to solve a game: {str(attempts - 1)}')
    else:
        print(f'game not solved before reaching max attempts {max_attempts}')


def generator(level, beautify=default_beautify):
    """
    the project main generator function
    :param level: level easy or medium
    :param beautify: default from settings.py
    :return: final sudoku game
    """
    attempts = 0
    max_attempts = common.level_to_attempts_mapper(level)
    while attempts <= max_attempts:
        try:
            obj = core.Core(rows=[])
            sudoku_grid = core.Core.grid_generator(obj)
            for sudoku_row in sudoku_grid:
                if bool(beautify):
                    #print(*sudoku_row)
                    print(*core.Core.row_mask(obj, sudoku_row, level))
                else:
                    print(core.Core.row_mask(obj, sudoku_row, level))
            attempts = attempts + 1
            break
        except ValueError:
            attempts = attempts + 1
            continue
        finally:
            if divmod(attempts, 100000)[1] == 1 and attempts > 1:
                print(f'attempts to generate a game: {str(attempts - 1)}')
    else:
        print(f'no game generated before reaching max attempts {max_attempts}')


r= [[0,3,0,0,8,5,4,9,1],
    [6,0,4,7,3,0,8,5,0],
    [0,9,0,1,4,2,7,0,3],
    [0,2,6,4,0,8,3,1,0],
    [0,4,3,0,0,1,9,7,8],
    [1,0,8,5,0,3,6,2,0],
    [3,6,0,8,0,0,5,4,9],
    [4,0,9,3,1,6,0,0,7],
    [7,8,0,0,5,0,1,3,6]]
"""
r= [[0,0,0,5,0,0,6,4,0],
    [0,0,9,6,3,0,0,1,8],
    [0,6,1,4,0,9,2,0,0],
    [0,0,0,0,0,1,8,0,3],
    [7,0,0,3,0,5,0,0,1],
    [2,0,3,9,0,0,0,0,0],
    [0,0,2,8,0,6,4,5,0],
    [6,7,0,0,5,4,3,0,0],
    [0,5,4,0,0,3,0,0,0]]

r= [[0,6,2,8,3,0,0,1,0],
    [0,0,9,0,0,0,0,2,0],
    [0,0,0,0,4,6,0,0,0],
    [0,5,1,6,7,0,8,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,7,0,1,2,6,5,0],
    [0,0,0,9,6,0,0,0,0],
    [0,1,0,0,0,0,2,0,0],
    [0,4,0,0,2,3,1,6,0]]
"""

if __name__ == '__main__':
    solver(rows_in=r)

"""
if __name__ == '__main__':
    # generator(level='easy')
    # generator(level='medium')
    # generator(level='hard')
"""
