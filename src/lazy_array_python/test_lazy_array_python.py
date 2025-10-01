from lazy_array_python import LazyArray

def test_lazy_array():
    # Test case 1
    arr1 = LazyArray([10, 20, 30, 40, 50])
    assert arr1.map(lambda n: n * 2).indexOf(40) == 1

    # Test case 2
    arr2 = LazyArray([10, 20, 30, 40, 50])
    assert arr2.map(lambda n: n * 2).map(lambda n: n * 3).indexOf(240) == 3

    # Test case 3
    arr3 = LazyArray([1, 2, 3, 4, 5])
    assert arr3.map(lambda n: n + 10).indexOf(100) == -1

    # Test case 4
    arr4 = LazyArray([5, 10, 15, 20, 25])
    assert arr4.map(lambda n: n * 2).map(lambda n: n + 5).map(lambda n: n // 3).indexOf(11) == 2

    # Test case 5
    arr5 = LazyArray([-5, 1, 2, -1, 10])
    assert arr5.map(lambda n: n * 3).map(lambda n: n + 4).map(lambda n: n - 2).indexOf(8) == 2

if __name__ == "__main__":
    test_lazy_array()