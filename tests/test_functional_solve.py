"""
functional testing solve sudoku pytest module
"""
import os

import pytest

from sudoku.sudoku_game import run_sudoku_solver


@pytest.mark.parametrize("test_input", [
    "sudoku_easy.txt",
    "sudoku_medium.txt",
    "sudoku_hard.txt",
    "sudoku_worlds_hardest.txt",
    "sudoku_4given_digits.txt",
    "sudoku_another_test_case_1.txt",
    "sudoku_another_test_case_2.txt",
    "sudoku_another_test_case_3.txt",
    "sudoku_another_test_case_4.txt",
    "sudoku_another_test_case_5.txt",
])
def test_solve_eval(test_input):
    """
    test we can solve all levels of a sudoku game
    :param test_input:
    :return:
    """
    target_file = os.path.join(os.getcwd(), 'files', test_input)
    solve = run_sudoku_solver(target_file, True)
    assert isinstance(solve, int)
