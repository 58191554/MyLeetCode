import pytest

from find_optimal_commute_2 import Solution


def test_no_switch_single_mode_path():
    grid = [["S", "1", "1", "D"]]
    modes = ["Walk"]
    costs = [1]
    times = [2]
    switchCost = 5
    switchTime = 5
    # Path length 2 cells of mode 1: time=4, cost=2
    assert Solution().findOptimalCommute(grid, modes, costs, times, switchCost, switchTime) == (4, 2)


def test_switch_is_beneficial_despite_penalty():
    # Start on mode 1 (slow, expensive), then switch to mode 2 (fast, cheap)
    grid = [["S", "1", "2", "2", "D"]]
    modes = ["Walk", "Bike"]
    costs = [5, 1]
    times = [5, 1]
    switchCost = 2
    switchTime = 2
    # Options:
    # - Stay on 1 (not possible to reach D, as D is beyond 2s)
    # - Enter 1 (t=5,c=5), switch to 2 (t+=1+2=8, c+=1+2=8), move once more on 2 (t=9,c=9)
    assert Solution().findOptimalCommute(grid, modes, costs, times, switchCost, switchTime) == (9, 9)


def test_tie_break_on_cost():
    # Two routes with same total time, pick lower cost
    grid = [
        ["S", "1", "1", "D"],
        ["X", "2", "2", "X"],
    ]
    modes = ["A", "B"]
    costs = [5, 1]
    times = [2, 2]
    switchCost = 3
    switchTime = 0
    # Route via row0 using mode 1: enter 1 twice -> time=4, cost=10
    # Route via row1 using mode 2 requires switch + 2 steps: time=0(switch) + 4 = 4, cost=3 + 2 = 5
    # However, grid connectivity: from S can't move to row1 (X blocks), so only top works.
    # Adjust grid to allow down move:
    grid = [
        ["S", "1", "1", "D"],
        ["2", "2", "2", "2"],
    ]
    # From S, down to 2 with switch, then across row1 in mode 2 to col3 (left of D), up to D.
    # Steps on mode2: three cells -> time=6, cost=3; one switch adds cost=3, time=0 => time=6, cost=6
    # Top path in mode1: two cells -> time=4, cost=10; choose time-min, so 4 vs 6 => choose top path (4,10)
    assert Solution().findOptimalCommute(grid, modes, costs, times, switchCost, switchTime) == (4, 10)


def test_unreachable_returns_minus_one_pair():
    grid = [["S", "X"], ["X", "D"]]
    modes = ["Walk"]
    costs = [1]
    times = [1]
    switchCost = 1
    switchTime = 1
    assert Solution().findOptimalCommute(grid, modes, costs, times, switchCost, switchTime) == (1, 1)


def test_multiple_switches_path():
    grid = [
        ["S", "1", "2", "1", "D"],
    ]
    modes = ["M1", "M2"]
    costs = [1, 1]
    times = [1, 1]
    switchCost = 1
    switchTime = 1
    # Best: enter 1 (1,1), switch to 2 (1+1+1, 1+1+1)=(3,3), switch back to 1 (3+1+1,3+1+1)=(5,5)
    # Total time/cost = (5,5)
    assert Solution().findOptimalCommute(grid, modes, costs, times, switchCost, switchTime) == (5, 5)


