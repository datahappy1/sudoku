import copy
from lib import core as core


def solver(rows_in=[], beautify=True):
    """
    the project main solver function
    :param rows_in: consuming list of lists with the sudoku to solve
    :param beautify: return list of lists as string
    :return: final solved sudoku
    """
    attempts = 0
    max_attempts = 50
    rows_ref = copy.deepcopy(rows_in)
    while attempts <= max_attempts:
        try:
            obj = core.Core(squares=[], rows=rows_ref)
            sudoku_grid = core.Core.grid_solver(obj)
            for sudoku_row in sudoku_grid:
                if bool(beautify):
                    print(*sudoku_row)
                else:
                    print(sudoku_row)
            attempts = attempts + 1
            break
        except ValueError:
            attempts = attempts + 1
            rows_ref = copy.deepcopy(rows_in)
            continue
        finally:
            if divmod(attempts, 1000)[1] == 1 and attempts > 1:
                print(f'attempts to solve a game: {str(attempts - 1)}')
    else:
        print(f'game not solved before reaching max attempts {max_attempts}')


def generator(level, beautify):
    """
    the project main generator function
    :param level: level easy or medium
    :param beautify: return list of lists as string
    :return: final sudoku game
    """
    attempts = 0
    max_attempts = 5000
    while attempts <= max_attempts:
        try:
            obj = core.Core(squares=[], rows=[])
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
            if divmod(attempts, 1000)[1] == 1 and attempts > 1:
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
if __name__ == '__main__':
    solver(rows_in=r)


"""
if __name__ == '__main__':
    # generator(level='easy', beautify=True)
    # generator(level='medium', beautify=True)
    generator(level='hard', beautify=True)
