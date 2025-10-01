import pytest

from find_fib_path import Solution


def test_example_1():
    order = 5
    source = 5
    dest = 7
    assert Solution().findPath(order, source, dest) == "UUURL"


def test_example_2():
    order = 4
    source = 8
    dest = 3
    assert Solution().findPath(order, source, dest) == "UUULR"


def test_example_3():
    order = 5
    source = 4
    dest = 13
    assert Solution().findPath(order, source, dest) == "UUURRRL"


def test_example_4():
    order = 2
    source = 2
    dest = 1
    assert Solution().findPath(order, source, dest) == "UL"


def test_example_5_same_node():
    order = 4
    source = 3
    dest = 3
    assert Solution().findPath(order, source, dest) == ""


def test_edge_same_node_min_order():
    order = 2
    source = 0
    dest = 0
    assert Solution().findPath(order, source, dest) == ""


def test_edge_within_same_subtree_small_order():
    # order=3 labels: 0(root), 1(L), 2(R), 3(RL), 4(RR)
    # 3 -> 4 : U then R
    order = 3
    source = 3
    dest = 4
    assert Solution().findPath(order, source, dest) == "UR"


def test_edge_root_to_deep_rightmost():
    # order=5 rightmost leaf label is 14; path is RRRR
    order = 5
    source = 0
    dest = 14
    assert Solution().findPath(order, source, dest) == "RRRR"


def test_edge_deep_left_to_root_then_left():
    # order=3: 4 -> 1 is UUL
    order = 3
    source = 4
    dest = 1
    assert Solution().findPath(order, source, dest) == "UUL"


def test_edge_within_left_fn2_subtree():
    # order=4 left Fn2 subtree labels: 1(rootL), 2(L of L), 3(R of L)
    # 2 -> 3 : U then R
    order = 4
    source = 2
    dest = 3
    assert Solution().findPath(order, source, dest) == "UR"


def test_edge_root_to_right_left_leaf():
    # order=3: 0 -> 3 is R then L
    order = 3
    source = 0
    dest = 3
    assert Solution().findPath(order, source, dest) == "RL"


