"""
sudoku.py
"""
import copy
import time
import argparse
from lib import core as core, common as common, gv as gv, ocr as ocr


def solver(sudoku_to_solve, prettify, verbose):
    """
    solver function
    :param sudoku_to_solve:
    :param prettify:
    :param verbose:
    :return: solved sudoku
    """
    rows_in = []
    gv.SUDOKU_VARIATIONS_AUX_SET = set()

    # load the sudoku from the txt file to a list of lists
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
            for sudoku_row in sudoku_grid:
                common.pretty_printer(prettify, sudoku_row)

        except common.CustomException as e:
            if str(e) == "TooManyCandidatesLeft":
                for variation in gv.SUDOKU_VARIATIONS_LIST:

                    if divmod(len(gv.SUDOKU_VARIATIONS_LIST), 10000)[1] == 1:
                        print(len(gv.SUDOKU_VARIATIONS_LIST))

                    obj = core.Core(action='solve', rows=variation)
                    try:
                        sudoku_grid = core.Core.grid_solver(obj)
                        if 0 not in sudoku_grid:
                            for sudoku_row in sudoku_grid:
                                common.pretty_printer(prettify, sudoku_row)
                            return 0

                    except common.CustomException:
                        gv.SUDOKU_VARIATIONS_LIST.remove(variation)

            # expected custom exception when no candidates are left, restart
            elif str(e) == "NoCandidatesLeft":
                break


#@verbose
def generator(level, prettify, verbose):
    """
    generator function
    :param level:
    :param prettify:
    :param verbose:
    :return: generated sudoku game
    """
    while True:
        try:
            obj = core.Core(action='generate', rows=[])
            sudoku_grid = core.Core.grid_generator(obj)
            for sudoku_row in sudoku_grid:
                masked_row = core.Core.row_mask(obj, sudoku_row, level)
                common.pretty_printer(prettify, masked_row)
            return 0

        # expected value error, no candidates left for the current grid
        # restart grid generator
        except ValueError:
            continue


def args_handler():
    """
    argparse arguments handler function
    :return:
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--action', type=str,
                        required=True,
                        choices={'solve', 'generate','ocr'})
    parser.add_argument('-l', '--generate_level', type=str,
                        required=False, default=None,
                        choices={'easy', 'medium', 'hard'})
    parser.add_argument('-f', '--file_with_sudoku_to_solve', type=str,
                        required=False, default=None)
    parser.add_argument('-p', '--prettify_output', type=str,
                        required=False, default=0)
    parser.add_argument('-v', '--verbose_printer_level', type=int,
                        required=False, default=0)

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
    elif action == 'ocr':
        ocr.ocr_core(sudoku_to_solve)


if __name__ == '__main__':
    args_handler()
