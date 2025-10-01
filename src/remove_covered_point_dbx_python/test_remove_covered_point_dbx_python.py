import pytest

from remove_covered_point_dbx_python import Solution


def test_remove_point_example_1_split_middle_interval():
    intervals = [[10, 12], [13, 16], [4, 8]]
    idx = 3
    expected = [[10, 12], [13, 14], [15, 16], [4, 8]]
    assert Solution().deleteCoveredPoint(intervals, idx) == expected


def test_remove_point_example_2_shrink_first_interval_start():
    intervals = [[4, 8], [13, 16], [10, 12]]
    idx = 0
    expected = [[5, 8], [13, 16], [10, 12]]
    assert Solution().deleteCoveredPoint(intervals, idx) == expected


def test_remove_point_example_3_shrink_end_of_first_interval():
    intervals = [[2, 6], [8, 10], [15, 18]]
    idx = 3
    expected = [[2, 5], [8, 10], [15, 18]]
    assert Solution().deleteCoveredPoint(intervals, idx) == expected


def test_remove_point_example_4_shrink_end_of_last_interval():
    intervals = [[1, 5], [7, 9], [12, 15]]
    idx = 8
    expected = [[1, 5], [7, 9], [12, 14]]
    assert Solution().deleteCoveredPoint(intervals, idx) == expected


def test_remove_point_example_5_split_middle_interval_adjacent_kept():
    intervals = [[1, 4], [5, 9], [10, 13]]
    idx = 4
    expected = [[1, 4], [5, 6], [7, 9], [10, 13]]
    assert Solution().deleteCoveredPoint(intervals, idx) == expected

