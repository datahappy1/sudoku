"""
sudoku_game.py
"""
import argparse
import datetime
from queue import LifoQueue
from sudoku import core, gv, common


def solver(sudoku_to_solve, prettify):
    """
    solver function
    :param sudoku_to_solve:
    :param prettify:
    :return: solved sudoku
    """
    rows_ref = []
    counter = 0

    # load the initial sudoku from the txt file to a list of lists
    with open(sudoku_to_solve) as file_handler:
        for row in file_handler:
            try:
                rows_ref.append([int(elem) for elem in row.join(row.split())])
            except ValueError as val_err:
                raise common.CustomException("InvalidGridItem {}".format(val_err)) from ValueError

    # validate the initial sudoku grid shape is 9x9
    if len(rows_ref) != 9 or any([len(y) != 9 for y in rows_ref]):
        raise common.CustomException("InvalidGridShape")

    gv.SUDOKU_VARIATIONS_QUEUE = LifoQueue()
    gv.SUDOKU_VARIATIONS_QUEUE.put_nowait(rows_ref)

    while not gv.SUDOKU_VARIATIONS_QUEUE.empty():
        variation = gv.SUDOKU_VARIATIONS_QUEUE.get_nowait()
        counter += 1
        if counter > 10000000:
            raise common.CustomException("TooManyTries")

        obj = core.Core(action='solve', rows=variation)
        try:
            sudoku_grid = core.Core.grid_solver(obj)
            for sudoku_row in sudoku_grid:
                common.pretty_printer(prettify, sudoku_row)
            return counter
        # expected custom exception when no candidates left or
        # too many candidates left for the current state of the grid ->
        # continue processing queue items with the grid solver
        except common.CustomException:
            continue


def generator(level, prettify):
    """
    generator function
    :param level:
    :param prettify:
    :return: generated sudoku game
    """
    counter = 0

    while True:
        counter += 1
        if counter > 10000000:
            raise common.CustomException("TooManyTries")

        try:
            obj = core.Core(action='generate', rows=[])
            sudoku_grid = core.Core.grid_generator(obj)
            for sudoku_row in sudoku_grid:
                masked_row = core.Core.row_mask(obj, sudoku_row, level)
                common.pretty_printer(prettify, masked_row)
            return counter
        # expected custom exception when no candidates left for the current grid
        # restart grid generator
        except common.CustomException:
            continue


def args_handler():
    """
    argparse arguments handler function
    :return: prepared_args
    """
    prepared_args = {}
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--action', type=str,
                        required=True,
                        choices={'solve', 'generate'})
    parser.add_argument('-l', '--generate_level', type=str,
                        required=False, default='easy',
                        choices={'easy', 'medium', 'hard'})
    parser.add_argument('-f', '--file_with_sudoku_to_solve', type=str,
                        required=False, default="files/sudoku_easy.txt")
    parser.add_argument('-p', '--prettify_output', type=str,
                        required=False, default='false')

    parsed = parser.parse_args()

    prepared_args['action'] = parsed.action
    prepared_args['generate_level'] = parsed.generate_level
    prepared_args['sudoku_to_solve'] = parsed.file_with_sudoku_to_solve

    prettify = parsed.prettify_output
    # arg parse bool data type known bug workaround
    if prettify.lower() in ('no', 'false', 'f', 'n', '0'):
        prepared_args['prettify'] = False
    else:
        prepared_args['prettify'] = True

    return prepared_args


if __name__ == '__main__':
    EXECUTION_START = datetime.datetime.now()

    PREPARED_ARGS = args_handler()
    ACTION = PREPARED_ARGS.get('action', None)
    GENERATE_LEVEL = PREPARED_ARGS.get('generate_level', None)
    SUDOKU_TO_SOLVE = PREPARED_ARGS.get('sudoku_to_solve', None)
    PRETTY = PREPARED_ARGS.get('prettify', None)
    RUNS_COUNT = 0

    if ACTION == 'generate':
        RUNS_COUNT = generator(GENERATE_LEVEL, PRETTY)
    elif ACTION == 'solve':
        RUNS_COUNT = solver(SUDOKU_TO_SOLVE, PRETTY)

    EXECUTION_END = datetime.datetime.now()
    print(f'Finished in {EXECUTION_END - EXECUTION_START} in {RUNS_COUNT} tries')
