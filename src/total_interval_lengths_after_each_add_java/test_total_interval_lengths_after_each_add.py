import pytest

from total_interval_lengths_after_each_add import total_lengths_after_each_add


def test_example_1_correct_total_lengths():
    # From README; corrected cumulative totals for closed intervals
    ops = [[1, 5], [10, 12], [3, 7], [12, 15], [8, 10]]
    assert total_lengths_after_each_add(ops) == [5, 8, 10, 13, 15]


def test_example_2_correct_total_lengths():
    # From README; corrected cumulative totals for closed intervals
    ops = [[5, 5], [6, 8], [2, 3], [4, 7]]
    assert total_lengths_after_each_add(ops) == [1, 4, 6, 7]


def test_adjacent_intervals_merge():
    ops = [[1, 2], [3, 4]]  # adjacent; should merge into [1,4]
    assert total_lengths_after_each_add(ops) == [2, 4]


def test_duplicate_addition_no_change():
    ops = [[1, 5], [1, 5]]
    assert total_lengths_after_each_add(ops) == [5, 5]


def test_contained_interval_no_increase():
    ops = [[1, 10], [3, 7]]
    assert total_lengths_after_each_add(ops) == [10, 10]


def test_negative_and_adjacent_merge():
    ops = [[-5, -3], [-2, 1]]  # -3 and -2 are adjacent; merge to [-5,1]
    assert total_lengths_after_each_add(ops) == [3, 7]


def test_large_ranges_and_overwrite():
    ops = [[1_000_000_000, 1_000_000_000], [-1_000_000_000, 1_000_000_000]]
    assert total_lengths_after_each_add(ops) == [1, 2_000_000_001]


def test_chain_merge_from_middle():
    ops = [[1, 2], [5, 6], [3, 4]]  # third bridges all -> [1,6]
    assert total_lengths_after_each_add(ops) == [2, 4, 6]


def test_bridge_separate_blocks():
    ops = [[1, 1], [5, 5], [2, 4]]  # final bridges to [1,5]
    assert total_lengths_after_each_add(ops) == [1, 2, 5]


