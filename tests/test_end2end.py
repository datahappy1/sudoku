"""
end to end pytest module
"""
from sudoku import generator, solver


def test_sudoku_gen():
    """
    lets generate a sudoku game
    """
    generated_game = generator('easy', True)
    assert generated_game == 0


def test_sudoku_solve_txt():
    """
    lets solve a txt file input sudoku game
    """
    solved_txt_game = solver('test_sudoku.txt', True)
    assert solved_txt_game == 0


#def test_sudoku_solve_ocr():
#    """
#    lets solve a ocr png file input sudoku game
#    """
#    solved_ocr_game = solver('test_sudoku.png', True)
#    assert solved_ocr_game == 0
