"""
functional testing generate and solve sudoku pytest module
"""
import os
from contextlib import redirect_stdout

import pytest

from sudoku.level import Level
from sudoku.sudoku_game import run_sudoku_generator, run_sudoku_solver


@pytest.mark.parametrize("test_input", [
    Level("easy"),
    Level("medium"),
    Level("hard"),
])
def test_generate_solve_eval(test_input):
    """
    test we can generate all levels of a sudoku game
    and solve them using the solver
    :param test_input:
    :return:
    """
    target_file = os.sep.join((os.getcwd(), "temp", test_input.value))

    with open(target_file, 'w') as f:
        with redirect_stdout(f):
            gen = run_sudoku_generator(test_input, True)
            assert isinstance(gen, int)

    file_content = []
    with open(target_file, 'r') as f:
        for line in f.readlines():
            file_content.append(line.replace(" ", ""))

    with open(target_file, 'w') as f:
        f.writelines(file_content)

    solve = run_sudoku_solver(target_file, True)
    assert isinstance(solve, int)
