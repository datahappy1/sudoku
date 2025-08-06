"""
grid
"""

from enum import Enum
from typing import List, Set, Tuple


class GridSolveStatus(Enum):
    TooManyCandidatesLeft = 0
    NoCandidatesLeft = 1


ALL_CANDIDATES_SET = {1, 2, 3, 4, 5, 6, 7, 8, 9}
ROW_INDEXES_SKIP_SQUARE_CALC = (0, 3, 6)

# {row_index:(related_row_index1, related_row_index2),}
# or
# {col_index:(related_col_index1, related_col_index2),}
GENERIC_GRID_MAP = {
    0: (1, 2),
    1: (0, 2),
    2: (0, 1),
    3: (4, 5),
    4: (3, 5),
    5: (3, 4),
    6: (7, 8),
    7: (6, 8),
    8: (6, 7),
}


def get_col_from_grid_rows(grid_rows: List[List[int]], col_index: int) -> Set[int]:
    """
    get column from grid represented in rows
    """
    return set(row[col_index] for row in grid_rows)


def _get_generic_grid_map_values_for_index(index: int) -> Tuple[int, int]:
    """
    grid offset mapping function
    this function takes row/col index and returns
    the related rows/cols
    """
    return GENERIC_GRID_MAP[index]


def get_square_from_position(
    grid_rows: List[List[int]], row_index: int, col_index: int
) -> Set[int]:
    """
    get square from position on grid except for the grid members from
    current row and col provided by the row_index/col_index arguments.
    for illustration, when provided row_index == 5 and col_index == 3 (marked below as `*`),
    this function returns a set containing the square members (marked below as `x`):

    =========
    =========
    =========
    ====xx===
    ====xx===
    ===*=====
    =========
    =========
    =========

    """
    square = set()
    related_row_index1, related_row_index2 = _get_generic_grid_map_values_for_index(
        index=row_index
    )
    related_column_index1, related_column_index2 = (
        _get_generic_grid_map_values_for_index(index=col_index)
    )

    try:
        square.add(grid_rows[related_row_index1][related_column_index1])
        square.add(grid_rows[related_row_index1][related_column_index2])
    except IndexError:
        # this is expected when generating grid, index error is raised for square
        # data lookups that are targeting rows/columns that haven't been yet populated
        pass

    try:
        square.add(grid_rows[related_row_index2][related_column_index1])
        square.add(grid_rows[related_row_index2][related_column_index2])
    except IndexError:
        # this is expected when generating grid, index error is raised for square
        # data lookups that are targeting rows/columns that haven't been yet populated
        pass

    return square
