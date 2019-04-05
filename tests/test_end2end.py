"""
end to end pytest module
"""
from sudoku import sudoku


class E2E:
    def __init__(self):
        self.generated_sudoku_game = None
        self.solved_sudoku_game = None

    def validate_sudoku_rows(self):
        pass

    def validate_sudoku_cols(self):
        pass

    def validate_sudoku_zeros(self):
        pass

    def setup(self):
        """
        lets generate a sudoku game
        """
        generate_level = 'easy'
        prettify = 'F'
        self.generated_sudoku_game = sudoku.generator(generate_level, prettify)
        print(self.generated_sudoku_game)

    def test_sudoku_generate_rowscount(self):
        E2E.validate_sudoku_rows()

    def test_sudoku_solve_basic(self):
        """
        assuming we can correctly solve the generated sudoku game
        and the result is a list
        """
        prettify = 'F'
        self.solved_sudoku_game = sudoku.solver(self.generated_sudoku_game, prettify)

        assert isinstance(self.solved_sudoku_game, list)

    def test_sudoku_solve_complex_colscount(self):
        """
        assuming we can correctly solve the generated sudoku game
        and the result has 9 columns in the grid
        """

        assert len(self.generated_sudoku_game) == 9

    def test_sudoku_solve_complex_rowscount(self):
        """
        assuming we can correctly solve the generated sudoku game
        and the result has 9 rows in the grid
        """

        assert len(self.generated_sudoku_game) == 9

    def test_sudoku_solve_complex_zeroscount(self):
        """
        assuming we can correctly solve the generated sudoku game
        and the result no zeros in the grid
        """

        assert len(self.generated_sudoku_game) == 9
