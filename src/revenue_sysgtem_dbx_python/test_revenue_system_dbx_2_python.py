import pytest

from revenue_system_dbx_2_python import RevenueSystem


def execute_ops(ops, args):
    results = []
    system = None
    for op, arg in zip(ops, args):
        if op == "RevenueSystem":
            system = RevenueSystem()
            results.append(None)
        elif op == "add":
            results.append(system.add(arg[0]))
        elif op == "addByReferral":
            results.append(system.addByReferral(arg[0], arg[1]))
        elif op == "getTopKCustomer":
            results.append(system.getTopKCustomer(arg[0], arg[1]))
        else:
            raise ValueError(f"Unknown op: {op}")
    return results


def test_example_1_from_readme():
    ops = [
        "RevenueSystem",
        "add",
        "add",
        "addByReferral",
        "addByReferral",
        "add",
        "getTopKCustomer",
        "addByReferral",
        "getTopKCustomer",
    ]
    args = [
        [],
        [100],
        [50],
        [30, 0],
        [70, 1],
        [50],
        [2, 100],
        [50, 4],
        [3, 100],
    ]

    expected = [None, 0, 1, 2, 3, 4, [0, 1], 5, [0, 1, 4]]
    assert execute_ops(ops, args) == expected


def test_example_2_from_readme():
    ops = [
        "RevenueSystem",
        "add",
        "addByReferral",
        "addByReferral",
        "addByReferral",
        "add",
        "addByReferral",
        "getTopKCustomer",
        "getTopKCustomer",
    ]
    args = [
        [],
        [100],
        [25, 0],
        [35, 0],
        [40, 0],
        [80],
        [30, 10],
        [2, 75],
        [3, 150],
    ]

    expected = [None, 0, 1, 2, 3, 4, -1, [0, 4], [0]]
    assert execute_ops(ops, args) == expected


def test_example_3_from_readme():
    ops = [
        "RevenueSystem",
        "add",
        "add",
        "addByReferral",
        "addByReferral",
        "add",
        "getTopKCustomer",
        "getTopKCustomer",
        "getTopKCustomer",
        "getTopKCustomer",
    ]
    args = [
        [],
        [20],
        [50],
        [40, 0],
        [30, 1],
        [10],
        [2, 100],
        [5, 15],
        [3, 50],
        [10, 1],
    ]

    expected = [None, 0, 1, 2, 3, 4, [], [1, 0, 2, 3], [1, 0], [1, 0, 2, 3, 4]]
    assert execute_ops(ops, args) == expected


def test_invalid_referrer_negative_and_out_of_range():
    system = RevenueSystem()
    assert system.add(10) == 0
    assert system.add(20) == 1
    assert system.addByReferral(5, -1) == -1  # invalid negative referrer
    assert system.add(30) == 2  # id continues without gap
    assert system.addByReferral(7, 10) == -1  # invalid out-of-range referrer
    assert system.add(40) == 3

    # Totals: id0=10, id1=20, id2=30, id3=40
    assert system.getTopKCustomer(10, 0) == [3, 2, 1, 0]


def test_k_zero_returns_empty_and_minRevenue_filters_all():
    system = RevenueSystem()
    system.add(5)
    system.add(15)
    system.add(25)

    assert system.getTopKCustomer(0, 0) == []  # k=0
    # Set threshold above any total revenue
    assert system.getTopKCustomer(5, 10_000) == []


def test_direct_referral_only_no_transitive_credit():
    system = RevenueSystem()
    a = system.add(100)  # 0
    b = system.add(0)    # 1
    c = system.addByReferral(30, a)  # 2, referrer 0 gets +30 => 130
    d = system.addByReferral(50, c)  # 3, referrer 2 gets +50 => 80. 0 should NOT get +50.

    assert [a, b, c, d] == [0, 1, 2, 3]
    # Totals expected: 0->130, 1->0, 2->80, 3->50
    assert system.getTopKCustomer(10, 0) == [0, 2, 3, 1]


def test_getTopK_limits_to_k_and_inclusive_minRevenue():
    system = RevenueSystem()
    id0 = system.add(10)
    id1 = system.add(35)
    id2 = system.add(20)

    # Inclusive threshold (>=)
    assert system.getTopKCustomer(5, 20) == [1, 2]
    # Limit to top-2 by revenue
    assert system.getTopKCustomer(2, 0) == [1, 2]


def test_multiple_referrals_accumulate_for_referrer():
    system = RevenueSystem()
    ref = system.add(10)              # 0 -> 10
    c1 = system.addByReferral(5, ref)  # 1 -> 5, ref total 15
    c2 = system.addByReferral(7, ref)  # 2 -> 7, ref total 22

    assert [ref, c1, c2] == [0, 1, 2]
    # Totals: 0->22, 1->5, 2->7
    assert system.getTopKCustomer(3, 0) == [0, 2, 1]


def test_large_k_more_than_existing_and_threshold_middle():
    system = RevenueSystem()
    system.add(12)   # 0
    system.add(3)    # 1
    system.add(25)   # 2
    system.add(8)    # 3

    # minRevenue=8 includes ids 0,2,3 in sorted order; k larger than available
    assert system.getTopKCustomer(10, 8) == [2, 0, 3]


def test_parent_and_children_relationships_and_invalids():
    system = RevenueSystem()
    a = system.add(100)          # 0
    b = system.addByReferral(30, a)  # 1, parent 0
    c = system.addByReferral(40, a)  # 2, parent 0
    d = system.addByReferral(50, b)  # 3, parent 1

    assert a == 0 and b == 1 and c == 2 and d == 3

    # Parents
    assert system.getReferer(a) == -1
    assert system.getReferer(b) == a
    assert system.getReferer(c) == a
    assert system.getReferer(d) == b
    assert system.getReferer(999) == -1

    # Children lists
    assert sorted(system.getChildren(a)) == [1, 2]
    assert sorted(system.getChildren(b)) == [3]
    assert system.getChildren(c) == []
    assert system.getChildren(d) == []
    assert system.getChildren(999) == []

