from typing import Dict, List, Iterator, Optional
from snapshot_set_iterator import SnapshotSet


# Helper function to iterate all elements in the iterator for easier visualization
def iterateAllElements(it: Iterator[int]) -> List[int]:
    return list(it)

def test1():
    print("======== test 1: =========")
    s = SnapshotSet()
    assert s.add(1) is True
    assert s.add(2) is True
    assert s.add(3) is True
    assert s.add(4) is True
    assert s.add(1) is False
    it1 = s.getIterator()
    assert s.remove(1) is True
    assert s.remove(3) is True
    assert s.remove(5) is False
    it2 = s.getIterator()

    assert iterateAllElements(it1) == [1, 2, 3, 4]
    assert iterateAllElements(it2) == [2, 4]

def test2():
    print("======== test 2: =========")
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

def test3():
    print("======== test 3: =========")
    s = SnapshotSet()
    assert s.remove(5) is False
    assert s.add(5) is True
    assert s.remove(5) is True
    assert s.add(5) is True
    assert iterateAllElements(s.getIterator()) == [5]

def test4():
    print("======== test 4: =========")
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
    assert iterateAllElements(it1) == [1, 2, 3, 4, 5]
    assert iterateAllElements(it2) == [1, 3, 5, 6]

if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
