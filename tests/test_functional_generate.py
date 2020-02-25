"""
functional testing generate sudoku pytest module
"""
import pytest
from sudoku.sudoku_game import generator


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
