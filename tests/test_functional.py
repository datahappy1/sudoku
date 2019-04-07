"""
functional testing pytest module
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


def test_sudoku_solve_txt_easy():
    """
    lets solve an easy level text file input sudoku game
    """
    target_file = os.path.join(os.getcwd(), 'tests', 'files', 'sudoku_easy.txt')
    solved_txt_game_easy = solver(target_file, True)
    assert solved_txt_game_easy == 0


def test_sudoku_solve_txt_medium():
    """
    lets solve a medium level text file input sudoku game
    """
    target_file = os.path.join(os.getcwd(), 'tests', 'files', 'sudoku_medium.txt')
    solved_txt_game_medium = solver(target_file, True)
    assert solved_txt_game_medium == 0


def test_sudoku_solve_txt_hard():
    """
    lets solve a hard level text file input sudoku game
    """
    target_file = os.path.join(os.getcwd(), 'tests', 'files', 'sudoku_hard.txt')
    solved_txt_game_hard = solver(target_file, True)
    assert solved_txt_game_hard == 0


#def test_sudoku_solve_ocr():
#    """
#    lets solve a ocr png file input sudoku game
#    """
#    solved_ocr_game = solver('test_sudoku.png', True)
#    assert solved_ocr_game == 0
