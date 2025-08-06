"""
solver
"""

import pickle
from typing import List, Set, Union, Optional
from collections import deque
from sudoku.exceptions import CustomException
from sudoku.grid import (
    GridSolveStatus,
    ALL_CANDIDATES_SET,
    get_square_from_position,
    get_col_from_grid_rows,
)
from sudoku.printer import pretty_printer

MAX_ATTEMPTS = 10000000


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


def _deepcopy_grid_rows(grid_rows: List[List[int]]) -> List[List[int]]:
    """
    deepcopy rows with pickle loads dumps function
    """
    return pickle.loads(pickle.dumps(grid_rows))


def _apply_candidate(
    grid_rows: List[List[int]], row_index: int, col_index: int, candidate: int
) -> List[List[int]]:
    """
    update rows with candidate function
    """
    grid_rows[row_index][col_index] = candidate
    return grid_rows


class Solver:
    """
    Solver class
    """

    def __init__(self):
        self.queue = deque()

    def _calculate_branch_pruning_threshold(self):
        """
        dynamic calculation to start pruning branches early based on queue size
        """
        branch_pruning_threshold = 4
        if len(self.queue) >= 100000:
            _bpt = branch_pruning_threshold + 1
            branch_pruning_threshold = min(_bpt, 9)
        elif len(self.queue) < 100000:
            _bpt = branch_pruning_threshold - 1
            branch_pruning_threshold = max(0, _bpt)
        return branch_pruning_threshold

    def _put_rows_to_queue(self, grid_rows: List[List[int]], is_priority: bool) -> None:
        """
        put rows to deque, if not priority, append left
        """
        if is_priority:
            self.queue.append(grid_rows)
        else:
            self.queue.appendleft(grid_rows)

    def _handle_multiple_candidates(
        self,
        grid_rows: List[List[int]],
        row_index: int,
        col_index: int,
        candidates_left: Set[int],
        priority: bool,
    ) -> GridSolveStatus:
        """
        handle multiple candidates
        """
        for candidate in candidates_left:
            updated_rows = _apply_candidate(
                grid_rows=_deepcopy_grid_rows(grid_rows),
                row_index=row_index,
                col_index=col_index,
                candidate=candidate,
            )
            self._put_rows_to_queue(updated_rows, priority)
        return GridSolveStatus.TooManyCandidatesLeft

    def _solve_grid(
        self, grid_rows: List[List[int]], branch_pruning_threshold: int
    ) -> Union[List[List[int]], GridSolveStatus]:
        """
        grid solver method
        """
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
                    elif len(candidates_left) <= branch_pruning_threshold:
                        return self._handle_multiple_candidates(
                            grid_rows=grid_rows,
                            row_index=row_index,
                            col_index=col_index,
                            candidates_left=candidates_left,
                            priority=True,
                        )
                    else:
                        return self._handle_multiple_candidates(
                            grid_rows=grid_rows,
                            row_index=row_index,
                            col_index=col_index,
                            candidates_left=candidates_left,
                            priority=False,
                        )
        return grid_rows

    def solve_sudoku(
        self, prettify: bool, initial_grid: List[List[int]]
    ) -> Optional[int]:
        """
        function responsible for the solving of the sudoku
        """
        counter = 0
        self.queue.append(initial_grid)
        while len(self.queue) != 0:
            variation = self.queue.pop()
            counter += 1
            if counter > MAX_ATTEMPTS:
                raise CustomException("TooManyTries")

            branch_pruning_threshold = self._calculate_branch_pruning_threshold()

            sudoku_grid = self._solve_grid(
                grid_rows=_deepcopy_grid_rows(variation),
                branch_pruning_threshold=branch_pruning_threshold,
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
