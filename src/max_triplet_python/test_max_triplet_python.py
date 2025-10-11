import pytest
from max_triplet_python import maxTriplets


def test_examples():
    assert maxTriplets([-4, 1, 0, -1, 0, 0, 0, 0, 0]) == 2
    assert maxTriplets([-1, 3, -1, 2, -1, 0, -3]) == 1
    assert maxTriplets([-1, -2, 3, -1, 0, 1]) == 2


def test_empty_and_small():
    assert maxTriplets([]) == 0
    assert maxTriplets([0]) == 0
    assert maxTriplets([0, 0]) == 0
    assert maxTriplets([0, 0, 0]) == 1


def test_overlap_choice():
    # Only non-overlapping allowed: choose indices (0,1,2) and (3,4,5)
    arr = [1, -1, 0, 2, -2, 0, 0]
    assert maxTriplets(arr) == 2


def test_no_zero_sum():
    assert maxTriplets([1, 1, 1, 1, 1, 1]) == 0


def test_multiple_options():
    # Many zeros: each consecutive triple is zero; greedy should pick non-overlapping
    arr = [0] * 9
    # possible to pick triples at 0,3,6 -> 3
    assert maxTriplets(arr) == 3
