"""
functional testing solve sudoku pytest module
"""
import os
import pytest
from sudoku.sudoku_game import solver


@pytest.mark.parametrize("test_input", [
    ("sudoku_easy.txt"),
    ("sudoku_medium.txt"),
    ("sudoku_hard.txt"),
])
def test_solve_eval(test_input):
    """
    test we can solve all levels of a sudoku game
    :param test_input:
    :return:
    """
    target_file = os.path.join(os.getcwd(), 'files', test_input)
    solve = str(solver(target_file, True))
    assert isinstance(eval(solve), int)
