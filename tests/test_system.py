"""
system testing pytest module
"""
from sudoku_game import generator, solver
import os


def test_sudoku_gen_easy():
    """
    lets generate an easy level sudoku game
    """
    generated_game_easy = generator('easy', True)
    assert generated_game_easy == 0


def test_sudoku_gen_medium():
    """
    lets generate a medium level sudoku game
    """
    generated_game_medium = generator('medium', True)
    assert generated_game_medium == 0


def test_sudoku_gen_hard():
    """
    lets generate a hard level sudoku game
    """
    generated_game_hard = generator('hard', True)
    assert generated_game_hard == 0


def test_sudoku_solve_txt():
    """
    lets solve a text file input sudoku game
    """
    target_file = os.path.join(os.getcwd(), 'tests', 'sudoku_test.txt')
    solved_txt_game = solver(target_file, True)
    assert solved_txt_game == 0


#def test_sudoku_solve_ocr():
#    """
#    lets solve a ocr png file input sudoku game
#    """
#    solved_ocr_game = solver('test_sudoku.png', True)
#    assert solved_ocr_game == 0
