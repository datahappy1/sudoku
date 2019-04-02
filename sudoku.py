"""
sudoku.py
"""
import copy
import time
import sys
import argparse
from lib import core as core, common as common, gv as gv


def solver(sudoku_to_solve, prettify, verbose):
    """

    :param sudoku_to_solve:
    :param prettify:
    :param verbose:
    :return:
    """

    def sudoku_printer(sudoku_grid):
        """

        :param sudoku_grid:
        :return:
        """
        for sudoku_row in sudoku_grid:
            if prettify is True:
                print(*sudoku_row)
            else:
                print(sudoku_row)
        sys.exit(0)

    rows_in = []
    with open(sudoku_to_solve) as f:
        for row in f:
            _ = []
            for elem in row.join(row.split()):
                _.append(int(elem))
            rows_in.append(_)

    rows_ref = copy.deepcopy(rows_in)

    while True:
        try:
            obj = core.Core(action='solve', rows=rows_ref)
            sudoku_grid = core.Core.grid_solver(obj)
            sudoku_printer(sudoku_grid)
        except common.CustomException as e:
            if str(e) == "TooManyCandidatesLeft":
                for variation in gv.sudoku_variations_list:
                    obj = core.Core(action='solve', rows=variation)
                    try:
                        sudoku_grid = core.Core.grid_solver(obj)
                        if 0 not in sudoku_grid:
                            sudoku_printer(sudoku_grid)
                    except common.CustomException:
                        gv.sudoku_variations_list.remove(variation)
            elif str(e) == "NoCandidatesLeft":
                break
            continue

@verbose
def generator(level, prettify, verbose):
    """

    :param level:
    :param prettify:
    :param verbose:
    :return:
    """
    while True:
        try:
            obj = core.Core(action='generate', rows=[])
            sudoku_grid = core.Core.grid_generator(obj)
            for sudoku_row in sudoku_grid:
                if prettify is True:
                    # print(*sudoku_row)
                    print(*core.Core.row_mask(obj, sudoku_row, level))
                else:
                    print(core.Core.row_mask(obj, sudoku_row, level))
            break
        except ValueError:
            continue


def args_handler():
    """

    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', type=str, required=True,
                        choices={'solve', 'generate'})
    parser.add_argument('-l', '--generate_level', type=str, required=False,
                        choices={'easy', 'medium', 'hard'}, default=None)
    parser.add_argument('-f', '--file_with_sudoku_to_solve', type=str, required=False, default=None)
    parser.add_argument('-p', '--prettify_output', type=str, required=False, default=0)
    parser.add_argument('-v', '--verbose_printer_level', type=str, required=False, default=0)

    parsed = parser.parse_args()

    action = parsed.action
    generate_level = parsed.generate_level
    sudoku_to_solve = parsed.file_with_sudoku_to_solve
    prettify = parsed.prettify_output
    verbose = parsed.verbose_printer_level

    # arg parse bool data type known bug workaround
    if prettify.lower() in ('no', 'false', 'f', 'n', 0):
        prettify = False
    else:
        prettify = True

    if action == 'generate':
        generator(generate_level, prettify, verbose)
    elif action == 'solve':
        solver(sudoku_to_solve, prettify, verbose)
    else:
        print('unknown action %s, terminating', action)
        sys.exit(1)


if __name__ == '__main__':
    args_handler()
