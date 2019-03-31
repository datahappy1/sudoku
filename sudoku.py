"""
sudoku.py
"""
import copy
import time
import sys
import argparse
from lib import core as core, common as common, gv as gv


def solver(sudoku_to_solve, prettify):
    """

    :param sudoku_to_solve:
    :param prettify:
    :return:
    """
    rows_in = []
    with open(sudoku_to_solve) as f:
        for row in f:
            row = row.split()
            rows_in.append(row)
    rows_in = str(rows_in).replace("'", "")

    print(rows_in)
    print(type(rows_in))

    rows_ref = copy.deepcopy(rows_in)

    while True:
        try:
            obj = core.Core(action='solve', rows=rows_ref)
            sudoku_grid = core.Core.grid_solver(obj)

            for sudoku_row in sudoku_grid:
                if prettify is True:
                    print(*sudoku_row)
                else:
                    print(sudoku_row)

            sys.exit(0)
        except common.CustomException as e:
            if str(e) == "TooManyCandidatesLeft":
                for ss in gv.s:
                    #print('ss', ss)
                    obj = core.Core(action='solve', rows=ss)
                    try:
                        o = core.Core.grid_solver(obj)
                        if 0 not in o:
                            print(o)
                            sys.exit(0)
                    except common.CustomException:
                        gv.s.remove(ss)
                        print(len(gv.s))
            elif str(e) == "NoCandidatesLeft":
                break
            continue


def generator(level, prettify):
    """

    :param level:
    :param prettify:
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


def main():
    """

    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-act', '--action', type=str, required=True,
                        choices={'solve', 'generate'})
    parser.add_argument('-glv', '--generate_level', type=str, required=False,
                        choices={'easy', 'medium', 'hard'}, default=None)
    parser.add_argument('-fws', '--file_with_sudoku_to_solve', type=str, required=False, default=None)
    parser.add_argument('-pro', '--prettify_output', type=str, required=False, default=0)

    parsed = parser.parse_args()

    action = parsed.action
    generate_level = parsed.generate_level
    sudoku_to_solve = parsed.file_with_sudoku_to_solve
    prettify = parsed.prettify_output

    # arg parse bool data type known bug workaround
    if prettify.lower() in ('no', 'false', 'f', 'n', 0):
        prettify = False
    else:
        prettify = True

    if action == 'generate':
        generator(generate_level, prettify)
    elif action == 'solve':
        solver(sudoku_to_solve, prettify)
    else:
        print('unknown action, terminating')
        sys.exit(1)


if __name__ == '__main__':
    main()
