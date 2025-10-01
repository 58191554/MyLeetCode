import pytest

from remove_covered_point_dbx_2_python import Solution


def test_single_op_equivalence_samples():
    # These mirror single-index cases, wrapped as single-element ops list
    assert Solution().deleteCoveredPoint([[10, 12], [13, 16], [4, 8]], [3]) == [
        [10, 12], [13, 14], [15, 16], [4, 8]
    ]
    assert Solution().deleteCoveredPoint([[4, 8], [13, 16], [10, 12]], [0]) == [
        [5, 8], [13, 16], [10, 12]
    ]
    assert Solution().deleteCoveredPoint([[2, 6], [8, 10], [15, 18]], [3]) == [
        [2, 5], [8, 10], [15, 18]
    ]
    assert Solution().deleteCoveredPoint([[1, 5], [7, 9], [12, 15]], [8]) == [
        [1, 5], [7, 9], [12, 14]
    ]
    assert Solution().deleteCoveredPoint([[1, 4], [5, 9], [10, 13]], [4]) == [
        [1, 4], [5, 6], [7, 9], [10, 13]
    ]


def test_multi_ops_sequential_delete_split_then_shrink():
    intervals = [[10, 12], [13, 16], [4, 8]]
    ops = [3, 0]
    # After idx=3 -> [[10,12],[13,14],[15,16],[4,8]]; then idx=0 removes 10 -> [11,12]
    expected = [[11, 12], [13, 14], [15, 16], [4, 8]]
    assert Solution().deleteCoveredPoint(intervals, ops) == expected


def test_multi_ops_remove_entire_interval_then_shrink_other():
    intervals = [[1, 2], [3, 5]]  # points: [1,3,4]
    ops = [0, 1]  # remove 1 (deletes first interval), then remove 4 (end of [3,5))
    expected = [[3, 4]]
    assert Solution().deleteCoveredPoint(intervals, ops) == expected


def test_multi_ops_split_then_shrink_same_original_interval():
    intervals = [[5, 9]]  # points: [5,6,7,8]
    ops = [1, 1]  # remove 6 -> split to [5,6],[7,9]; then remove 7 -> [8,9]
    expected = [[5, 6], [8, 9]]
    assert Solution().deleteCoveredPoint(intervals, ops) == expected


def test_multi_ops_across_three_intervals_mixed_edges():
    intervals = [[2, 6], [8, 10], [15, 18]]
    ops = [3, 0, 4]
    # Step1 idx=3 -> [[2,5],[8,10],[15,18]]; Step2 idx=0 -> [[3,5],[8,10],[15,18]];
    # Step3 idx=4 -> removes 15 -> [[3,5],[8,10],[16,18]]
    expected = [[3, 5], [8, 10], [16, 18]]
    assert Solution().deleteCoveredPoint(intervals, ops) == expected


def test_multi_ops_split_middle_and_later_shrink_that_segment():
    intervals = [[1, 4], [5, 9], [10, 13]]  # points: [1,2,3,5,6,7,8,10,11,12]
    ops = [4, 4]
    # Step1 removes 6 -> [[1,4],[5,6],[7,9],[10,13]]
    # New points: [1,2,3,5,7,8,10,11,12]
    # Step2 removes 7 -> shrink [7,9] to [8,9]
    expected = [[1, 4], [5, 6], [8, 9], [10, 13]]
    assert Solution().deleteCoveredPoint(intervals, ops) == expected
