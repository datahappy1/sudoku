"""
functional testing generate sudoku pytest module
"""
import pytest
from sudoku.sudoku_game import run_sudoku_generator


@pytest.mark.parametrize("test_input", [
    "easy",
    "medium",
    "hard",
])
def test_generate_eval(test_input):
    """
    test we can generate all levels of a sudoku game
    :param test_input:
    :return:
    """
    gen = run_sudoku_generator(test_input, True)
    assert isinstance(gen, int)
