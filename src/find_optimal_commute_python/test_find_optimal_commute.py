import pytest

from find_optimal_commute import Solution


def test_example_1_bike_is_best():
    grid = [["3","3","S","2","X","X"],
            ["3","1","1","2","X","2"],
            ["3","1","1","2","2","2"],
            ["3","1","1","1","D","3"],
            ["3","3","3","3","3","4"],
            ["4","4","4","4","4","4"]]
    modes = ["Walk","Bike","Car","Train"]
    costs = [0,1,3,2]
    times = [3,2,1,1]
    assert Solution().findOptimalCommute(grid, modes, costs, times) == "Bike"


def test_example_2_bike_in_middle_row():
    grid = [["S","1","1"],
            ["2","2","2"],
            ["D","1","1"]]
    modes = ["Walk","Bike","Car","Train"]
    costs = [0,1,3,2]
    times = [2,2,1,1]
    assert Solution().findOptimalCommute(grid, modes, costs, times) == "Bike"


def test_example_3_unreachable_returns_empty():
    grid = [["S","1","X"],
            ["X","3","3"],
            ["2","2","D"]]
    modes = ["Walk","Bike","Car"]
    costs = [0,1,3,2]
    times = [3,2,1,1]
    assert Solution().findOptimalCommute(grid, modes, costs, times) == ""


def test_small_grid_prefers_walk():
    grid = [["S","2"],
            ["1","D"]]
    modes = ["Walk","Car"]
    costs = [0,3]
    times = [1,1]
    assert Solution().findOptimalCommute(grid, modes, costs, times) == "Walk"


def test_larger_grid_train_best_time():
    grid = [["S","4","4","4","4"],
            ["1","4","2","3","4"],
            ["1","4","2","3","4"],
            ["1","4","2","3","4"],
            ["1","1","1","1","D"]]
    modes = ["Train","Car","Walk","Bike"]
    costs = [2,3,0,1]
    times = [1,3,5,4]
    assert Solution().findOptimalCommute(grid, modes, costs, times) == "Train"


def test_unreachable_start_boxed_by_blocks():
    grid = [["X","X","X"],
            ["X","S","X"],
            ["X","D","X"]]
    modes = ["Walk"]
    costs = [0]
    times = [1]
    assert Solution().findOptimalCommute(grid, modes, costs, times) == "Walk"


def test_unreachable_dest_boxed_by_blocks():
    grid = [["S","1","X"],
            ["1","X","X"],
            ["X","D","X"]]
    modes = ["Walk"]
    costs = [0]
    times = [1]
    assert Solution().findOptimalCommute(grid, modes, costs, times) == ""


def test_single_mode_straight_corridor():
    grid = [["S","1","1","1","D"]]
    modes = ["Walk"]
    costs = [0]
    times = [1]
    assert Solution().findOptimalCommute(grid, modes, costs, times) == "Walk"


def test_many_modes_only_one_present_in_grid():
    grid = [["S","1","1","D"]]
    modes = ["Walk","Bike","Car","Train","Scooter"]
    costs = [0,5,5,5,5]
    times = [1,1,1,1,1]
    assert Solution().findOptimalCommute(grid, modes, costs, times) == "Walk"


def test_minimal_adjacency_no_digits_between_returns_empty():
    grid = [["S","D"]]
    modes = ["Walk"]
    costs = [0]
    times = [1]
    assert Solution().findOptimalCommute(grid, modes, costs, times) == "Walk"


