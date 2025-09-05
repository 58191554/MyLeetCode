from typing import List, Iterator
import os
import sys

# Ensure this test runs regardless of current working directory
CURRENT_DIR = os.path.dirname(__file__)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from snapshot_set_iterator import SnapshotSet


# Helper: collect all elements from the iterator
def iterateAllElements(it: Iterator[int]) -> List[int]:
    return list(it)


def test_basic_add_remove_and_iterators():
    s = SnapshotSet()

    assert s.add(1) is True
    assert s.add(2) is True
    assert s.add(3) is True
    assert s.add(4) is True
    assert s.add(1) is False  # duplicate add

    it1 = s.getIterator()

    assert s.remove(1) is True
    assert s.remove(3) is True
    assert s.remove(5) is False  # non-existent

    it2 = s.getIterator()

    assert iterateAllElements(it1) == [1, 2, 3, 4]
    assert iterateAllElements(it2) == [2, 4]


def test_iterators_at_various_times():
    s = SnapshotSet()

    it1 = s.getIterator()
    assert s.add(10) is True
    it2 = s.getIterator()
    assert s.add(20) is True
    it3 = s.getIterator()
    assert s.add(30) is True
    it4 = s.getIterator()
    assert s.remove(30) is True
    it5 = s.getIterator()
    assert s.remove(20) is True
    it6 = s.getIterator()
    assert s.remove(10) is True
    it7 = s.getIterator()

    assert iterateAllElements(it1) == []
    assert iterateAllElements(it2) == [10]
    assert iterateAllElements(it3) == [10, 20]
    assert iterateAllElements(it4) == [10, 20, 30]
    assert iterateAllElements(it5) == [10, 20]
    assert iterateAllElements(it6) == [10]
    assert iterateAllElements(it7) == []


def test_remove_then_add_same_value():
    s = SnapshotSet()

    assert s.remove(5) is False  # not present
    assert s.add(5) is True
    assert s.remove(5) is True
    assert s.add(5) is True  # can re-add after removal
    assert iterateAllElements(s.getIterator()) == [5]


def test_mixed_operations_and_ordering():
    s = SnapshotSet()

    assert s.add(1) is True
    assert s.add(2) is True
    assert s.add(3) is True
    assert s.add(4) is True
    assert s.add(5) is True

    it1 = s.getIterator()

    assert s.remove(2) is True
    assert s.remove(4) is True
    assert s.add(6) is True

    it2 = s.getIterator()

    # it1 should see the original snapshot
    assert iterateAllElements(it1) == [1, 2, 3, 4, 5]
    # it2 sees the new state
    assert iterateAllElements(it2) == [1, 3, 5, 6]
