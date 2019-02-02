"""
test end 2 end
"""
import pytest
from sudoku import generator as gen
from sudoku import solver as solve

"""
@pytest.fixture='easy'
def generate_sudoku():
    pass


def solve_sudoku():
    pass

"""


def test_e2e():
    """
    assuming the sudoku gets generated and solved
    :return: assertion result
    """
    #TODO FUNCTION MAIN SOLVER,GEN MUST RETURN NOT PRINT!!
    rows_gen = gen(level='easy', beautify=False)
    #rows_solve = \
    #solve(rows_in=rows_gen)

    #print(rows_gen)
    #print(rows_solve)

    #assert 1 == 1


test_e2e()
