"""
end to end pytest module
"""
from sudoku import sudoku


class E2E:
    def __init__(self):
        self.generated_sudoku_game = []

    def setup(self):
        """
        lets generate a sudoku game
        """
        generate_level = 'easy'
        prettify = 'F'
        self.generated_sudoku_game = sudoku.generator(generate_level, prettify)
        print(self.generated_sudoku_game)

    def test_sudoku_solve(self):
        """
        assuming we can correctly solve the generated sudoku game
        """
        prettify = 'F'
        solved_sudoku_game = sudoku.solver(self.generated_sudoku_game, prettify)

        assert isinstance(solved_sudoku_game, list)

