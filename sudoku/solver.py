"""
solver
"""

from queue import PriorityQueue
from typing import List, Set, Union, Optional

from sudoku.exceptions import CustomException
from sudoku.grid import (
    GridSolveStatus,
    ALL_CANDIDATES_SET,
    get_square_from_position,
    get_col_from_grid_rows,
)
from sudoku.printer import pretty_printer

MAX_ATTEMPTS = 1000000


def _get_candidates(
    grid_rows: List[List[int]], row_index: int, col_index: int
) -> Set[int]:
    """
    get solver cell candidates function
    """
    return (
        ALL_CANDIDATES_SET
        - set(grid_rows[row_index])
        - get_square_from_position(grid_rows, row_index, col_index)
        - get_col_from_grid_rows(grid_rows, col_index)
    )


def _apply_candidate(
    grid_rows: List[List[int]], row_index: int, col_index: int, candidate: int
) -> List[List[int]]:
    """
    update rows with candidate function
    """
    new_grid_rows = [x[:] for x in grid_rows]
    new_grid_rows[row_index][col_index] = candidate
    return new_grid_rows


class Solver:
    """
    Solver class
    """

    def __init__(self):
        self.queue = PriorityQueue()

    def _put_rows_to_queue(self, grid_rows: List[List[int]], priority: int) -> None:
        """
        put rows to queue with priority
        """
        self.queue.put((priority, grid_rows))

    def _handle_multiple_candidates(
        self,
        grid_rows: List[List[int]],
        row_index: int,
        col_index: int,
        candidates_left: Set[int],
        priority: int,
    ) -> None:
        """
        handle multiple candidates
        """
        for candidate in candidates_left:
            updated_rows = _apply_candidate(
                grid_rows=grid_rows,
                row_index=row_index,
                col_index=col_index,
                candidate=candidate,
            )
            self._put_rows_to_queue(updated_rows, priority)
        return

    def _solve_grid(
        self, grid_rows: List[List[int]]
    ) -> Union[List[List[int]], GridSolveStatus]:
        """
        grid solver method
        """
        unknowns_count = len({e for r in grid_rows for e in r if e == 0})

        for row_index, row in enumerate(grid_rows):
            for col_index in range(0, 9):
                if row[col_index] == 0:
                    candidates_left = _get_candidates(
                        grid_rows=grid_rows, row_index=row_index, col_index=col_index
                    )

                    if not candidates_left:
                        return GridSolveStatus.NoCandidatesLeft

                    if len(candidates_left) == 1:
                        row[col_index] = candidates_left.pop()
                    else:
                        self._handle_multiple_candidates(
                            grid_rows=grid_rows,
                            row_index=row_index,
                            col_index=col_index,
                            candidates_left=candidates_left,
                            priority=unknowns_count,
                        )
                        return GridSolveStatus.TooManyCandidatesLeft
        return grid_rows

    def solve_sudoku(
        self, prettify: bool, initial_grid: List[List[int]]
    ) -> Optional[int]:
        """
        function responsible for the solving of the sudoku
        """
        counter = 0
        self.queue.put((0, initial_grid))
        while not self.queue.empty():
            variation = self.queue.get()[1]
            counter += 1
            if counter > MAX_ATTEMPTS:
                raise CustomException("TooManyTries")

            sudoku_grid = self._solve_grid(
                grid_rows=variation,
            )
            if sudoku_grid in (
                GridSolveStatus.NoCandidatesLeft,
                GridSolveStatus.TooManyCandidatesLeft,
            ):
                continue
            for sudoku_row in sudoku_grid:
                pretty_printer(prettify, sudoku_row)
            return counter
        return None
