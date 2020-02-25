"""
sudoku_game.py
"""
import argparse
import datetime
from lib import core, common, gv


def solver(sudoku_to_solve, prettify):
    """
    solver function
    :param sudoku_to_solve:
    :param prettify:
    :return: solved sudoku
    """
    rows_ref = []
    gv.SUDOKU_VARIATIONS_AUX_SET = set()

    # load the sudoku from the txt file to a list of lists
    with open(sudoku_to_solve) as file_handler:
        for row in file_handler:
            rows_ref.append([int(elem) for elem in row.join(row.split())])

    gv.SUDOKU_VARIATIONS_LIST.insert(0, rows_ref)

    while True:
        for variation_index, variation in enumerate(gv.SUDOKU_VARIATIONS_LIST):
            obj = core.Core(action='solve', rows=variation)
            try:
                sudoku_grid = core.Core.grid_solver(obj)
                if 0 not in sudoku_grid:
                    for sudoku_row in sudoku_grid:
                        common.pretty_printer(prettify, sudoku_row)
                    return 0

            except common.CustomException:
                gv.SUDOKU_VARIATIONS_LIST.pop(variation_index)


def generator(level, prettify):
    """
    generator function
    :param level:
    :param prettify:
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

        # expected custom exception when no candidates left for the current grid
        # restart grid generator
        except common.CustomException:
            continue


def args_handler():
    """
    argparse arguments handler function
    :return:
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--action', type=str,
                        required=True,
                        choices={'solve', 'generate', 'ocr'})
    parser.add_argument('-l', '--generate_level', type=str,
                        required=False, default='easy',
                        choices={'easy', 'medium', 'hard'})
    parser.add_argument('-f', '--file_with_sudoku_to_solve', type=str,
                        required=False, default="files/sudoku_easy.txt")
    parser.add_argument('-p', '--prettify_output', type=str,
                        required=False, default='false')

    parsed = parser.parse_args()

    action = parsed.action
    generate_level = parsed.generate_level
    sudoku_to_solve = parsed.file_with_sudoku_to_solve
    prettify = parsed.prettify_output

    # arg parse bool data type known bug workaround
    if prettify.lower() in ('no', 'false', 'f', 'n', '0'):
        prettify = False
    else:
        prettify = True

    if action == 'generate':
        generator(generate_level, prettify)
    elif action == 'solve':
        solver(sudoku_to_solve, prettify)


if __name__ == '__main__':
    EXECUTION_START = datetime.datetime.now()
    args_handler()
    EXECUTION_END = datetime.datetime.now()
    print(f'Finished in {EXECUTION_END - EXECUTION_START}')
