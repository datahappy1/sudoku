"""
functional testing pytest module
"""
import os
import pytest
from sudoku_game import generator, solver


@pytest.mark.parametrize("test_input,expected", [
    ("easy", 0),
    ("medium", 0),
    ("hard", 0),
])
def test_generate_eval(test_input, expected):
    """
    test we can generate all levels of a sudoku game
    :param test_input:
    :param expected:
    :return:
    """
    gen = str(generator(test_input, True))
    assert eval(gen) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("sudoku_easy.txt", 0),
    ("sudoku_medium.txt", 0),
    ("sudoku_hard.txt", 0),
])
def test_solve_eval(test_input, expected):
    """
    test we can solve all levels of a sudoku game
    :param test_input:
    :param expected:
    :return:
    """
    target_file = os.path.join(os.getcwd(), 'files', test_input)
    solve = str(solver(target_file, True))
    assert eval(solve) == expected
