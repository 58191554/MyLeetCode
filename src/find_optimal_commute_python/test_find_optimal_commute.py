import pytest

from find_optimal_commute import Solution


def test_example_from_doc():
    # Grid from the problem statement
    grid = [
        [1, 2, 1],
        [1, 3, 2],
        [1, 1, 1],
    ]
    # 1-indexed vectors; put a 0 at index 0 for alignment
    time = [0, 1, 2, 4]
    cost = [0, 3, 1, 5]
    start = (0, 0)
    end = (2, 2)

    # Expected: choose path along 1-cells at the bottom/left: total time 4, cost 12
    assert Solution.find_optimal_commute(grid, time, cost, start, end) == (4, 12)


def test_tiebreaker_prefers_lower_cost():
    # Construct a grid where multiple shortest-time paths exist (all moves cost 1 time),
    # but costs differ; prefer path with more mode-2 cells which are cheaper.
    grid = [
        [1, 2, 2],
        [1, 2, 2],
        [1, 1, 1],
    ]
    time = [0, 1, 1]  # both modes take 1 minute
    cost = [0, 5, 0]  # mode 1 is expensive, mode 2 is free
    start = (0, 0)
    end = (2, 2)

    # Minimal time is 4 for any shortest path.
    # Cheapest of those is Right,Right,Down,Down through many mode-2 cells: total cost 5.
    assert Solution.find_optimal_commute(grid, time, cost, start, end) == (4, 5)


def test_start_equals_end():
    grid = [
        [1, 2],
        [2, 1],
    ]
    time = [0, 1, 2]
    cost = [0, 3, 1]
    start = (0, 0)
    end = (0, 0)

    # No movement → zero time and cost
    assert Solution.find_optimal_commute(grid, time, cost, start, end) == (0, 0) 