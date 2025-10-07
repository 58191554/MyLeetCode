import pytest

from deficiency_bottle_neck_python import Solution


def test_example_1_single_root_bottleneck():
    n = 5
    edges = [[0, 1], [0, 2], [1, 3], [1, 4]]
    expected = [0]
    assert sorted(Solution().findBottlenecks(n, edges)) == sorted(expected)


def test_example_2_chain_all_bottlenecks():
    n = 4
    edges = [[0, 1], [1, 2], [2, 3]]
    expected = [0, 1, 2, 3]
    assert sorted(Solution().findBottlenecks(n, edges)) == sorted(expected)


def test_example_3_parallel_pairs_no_bottleneck():
    n = 6
    edges = [[0, 1], [2, 3], [4, 5]]
    expected = []
    assert sorted(Solution().findBottlenecks(n, edges)) == sorted(expected)


def test_example_4_single_node_graph():
    n = 1
    edges = []
    expected = [0]
    assert sorted(Solution().findBottlenecks(n, edges)) == sorted(expected)


def test_example_5_mixed_graph_multiple_bottlenecks():
    n = 7
    edges = [[0, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 5], [2, 3], [5, 6]]
    expected = [0, 5, 6]
    assert sorted(Solution().findBottlenecks(n, edges)) == sorted(expected)


