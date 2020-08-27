"""
sudoku_game.py
"""
import argparse
import datetime

from sudoku import core
from sudoku.exceptions import CustomException


def run_sudoku_solver(sudoku_to_solve, prettify):
    """
    solver function
    :param sudoku_to_solve:
    :param prettify:
    :return: solved sudoku
    """
    def open_file(sudoku):
        """
        open the initial sudoku
        from the txt file and return a list of lists
        with the grid items
        :param sudoku:
        :return:
        """
        sudoku_grid = []
        with open(sudoku) as file_handler:
            for row in file_handler:
                sudoku_grid.append(validate_row(row))
        return sudoku_grid

    def validate_row(row):
        """
        validate row is a list of integers
        :param row:
        :return:
        """
        try:
            row = [int(elem) for elem in row.join(row.split())]
        except ValueError as val_err:
            raise CustomException("InvalidGridItem {}".format(val_err)) \
                from ValueError
        return row

    def validate_grid_shape(sudoku_grid):
        """
        validate the initial sudoku grid shape is 9x9
        :param sudoku_grid:
        :return:
        """
        if len(sudoku_grid) != 9 or \
                any([len(y) != 9 for y in sudoku_grid]):
            raise CustomException("InvalidGridShape")

        return sudoku_grid

    loaded_sudoku_grid = open_file(sudoku_to_solve)
    validated_sudoku_grid = validate_grid_shape(loaded_sudoku_grid)

    sudoku_obj = core.Core(action='solve')
    counter = sudoku_obj.sudoku_solver(prettify=prettify, initial_grid=validated_sudoku_grid)
    return counter


def run_sudoku_generator(level, prettify):
    """
    generator function
    :param level:
    :param prettify:
    :return: generated sudoku game
    """
    sudoku_obj = core.Core(action='generate')
    counter = sudoku_obj.sudoku_generator(prettify=prettify, level=level)
    return counter


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
        RUNS_COUNT = run_sudoku_generator(GENERATE_LEVEL, PRETTY)
    elif ACTION == 'solve':
        RUNS_COUNT = run_sudoku_solver(SUDOKU_TO_SOLVE, PRETTY)

    EXECUTION_END = datetime.datetime.now()
    print(f'Finished in {EXECUTION_END - EXECUTION_START} in {RUNS_COUNT} tries')
