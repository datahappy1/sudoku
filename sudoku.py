import copy
import queue
from lib import core as core, common as common, gv as gv


def solver(rows_in):
    attempts = 0
    failed_attempts = 0
    gv.q = queue.Queue()
    max_attempts = common.level_to_attempts_mapper(level='default')
    rows_ref = copy.deepcopy(rows_in)
    while attempts <= max_attempts:
        try:
            obj = core.Core(action='solve', rows=rows_ref)
            sudoku_grid = core.Core.grid_solver(obj)
            for sudoku_row in sudoku_grid:
                # print(*sudoku_row)
                print(sudoku_row)
            attempts = attempts + 1
            print(attempts)
            break
        except common.CustomException as e:
            if str(e) == "NoCandidatesLeft":
                rows_ref = copy.deepcopy(rows_in)
                failed_attempts += 1

            elif str(e) == "TooManyCandidatesLeft":
                # print(attempts, rows_ref)
                if failed_attempts == 5000:
                    gv.unknown_cell_index = [0, 0]
                gv.unknown_cell_index = [gv.unknown_cell_index[0], gv.unknown_cell_index[1]-1]
            attempts = attempts + 1
            failed_attempts = failed_attempts + 1
            continue
        finally:
            if divmod(attempts, 10000)[1] == 1 and attempts > 1:
                print(f'attempts to solve a game: {str(attempts - 1)}')
    else:
        print(f'game not solved before reaching max attempts {max_attempts}')


def queue_processor():
    if not gv.q.empty():
        for _ in iter(gv.q.get, None):
            rows_ref = copy.deepcopy(gv.q.get())
            #print(rows_ref)
            solver(rows_ref)


def generator(level):
    attempts = 0
    max_attempts = common.level_to_attempts_mapper(level)
    while attempts <= max_attempts:
        try:
            obj = core.Core(action='generate', rows=[])
            sudoku_grid = core.Core.grid_generator(obj)
            for sudoku_row in sudoku_grid:
                #print(*sudoku_row)
                #print(*core.Core.row_mask(obj, sudoku_row, level))
                print(core.Core.row_mask(obj, sudoku_row, level))
            attempts = attempts + 1
            print(attempts)
            break
        except ValueError:
            attempts = attempts + 1
            continue
        finally:
            if divmod(attempts, 10000)[1] == 1 and attempts > 1:
                print(f'attempts to generate a game: {str(attempts - 1)}')
    else:
        print(f'no game generated before reaching max attempts {max_attempts}')


def main(action, level=None, rows_in=None):
    if action == 'generate':
        generator(level)
    elif action == 'solve':
        solver(rows_in=rows_in)
        queue_processor()

r= [[4,0,0,0,0,7,0,8,0],
    [0,8,0,0,0,0,2,0,1],
    [0,0,0,6,8,0,5,0,4],
    [0,0,5,0,0,1,0,0,6],
    [0,0,0,0,9,0,0,0,0],
    [2,0,0,5,0,0,7,0,0],
    [5,0,2,0,7,3,0,0,0],
    [1,0,9,0,0,0,0,4,0],
    [0,6,0,4,0,0,0,0,7]]

if __name__ == '__main__':
    #main(action='generate', level='easy')
    #main(action='generate', level='medium')
    #main(action='generate', level='hard')
    main(action='solve', rows_in=r)
