from typing import Tuple
from find_fib_path.find_fib_path import TreeNode
import pytest


def create_tree(n: int, x: int) -> Tuple[TreeNode, int]:
    if n == 1 or n == 0:
        return TreeNode(x, n), 1
    node = TreeNode(x, n)
    l_node, l_num = create_tree(n - 2, x + 1)
    r_node, r_num = create_tree(n - 1, x + l_num + 1)
    node.l = l_node
    node.r = r_node
    return node, l_num + r_num + 1

# Helpers for tests

def find_path_in_tree(root: TreeNode, start: int, end: int) -> str:
    # Build parent map and find references to start and end
    parent = {root: None}
    node_by_val = {root.val: root}

    stack = [root]
    while stack:
        node = stack.pop()
        if node.l:
            parent[node.l] = node
            node_by_val[node.l.val] = node.l
            stack.append(node.l)
        if node.r:
            parent[node.r] = node
            node_by_val[node.r.val] = node.r
            stack.append(node.r)

    start_node = node_by_val[start]
    end_node = node_by_val[end]

    # Path from root to nodes
    def path_to_root(n: TreeNode):
        p = []
        while n is not None:
            p.append(n)
            n = parent[n]
        p.reverse()
        return p

    ps = path_to_root(start_node)
    pe = path_to_root(end_node)

    # Find LCA
    i = 0
    while i < len(ps) and i < len(pe) and ps[i] is pe[i]:
        i += 1
    lca_idx = i - 1

    # Moves up from start to LCA
    ups = len(ps) - 1 - lca_idx

    # Moves down from LCA to end
    moves_down = []
    for j in range(lca_idx + 1, len(pe)):
        parent_node = pe[j - 1]
        child_node = pe[j]
        if parent_node.l is child_node:
            moves_down.append('L')
        else:
            moves_down.append('R')

    return 'U' * ups + ''.join(moves_down)


def test_single_node_orders():
    from find_fib_path.find_fib_path import Solution

    sol = Solution()

    # Order 0 and 1 trees: only one node (label 0)
    root0, _ = create_tree(0, 0)
    assert sol.find_fib_path(0, 0, root0) == ""

    root1, _ = create_tree(1, 0)
    assert sol.find_fib_path(0, 0, root1) == ""


_cases = [
    (0, 0),
    (0, 1),
    (1, 0),
    (2, 3),
    # (5, 7) is covered by a dedicated test below
    (7, 5),
    (3, 8),
    (8, 3),
    (6, 6),
]


@pytest.mark.parametrize("s,e", _cases, ids=[f"{s}->{e}" for s, e in _cases])
def test_paths_match_ground_truth(s: int, e: int):
    from find_fib_path.find_fib_path import Solution

    sol = Solution()
    root5, _ = create_tree(5, 0)
    expected = find_path_in_tree(root5, s, e)
    got = sol.find_fib_path(s, e, root5)
    assert got == expected


def test_given_example_5_to_7():
    from find_fib_path.find_fib_path import Solution
    sol = Solution()
    root, _ = create_tree(5, 0)
    assert sol.find_fib_path(5, 7, root) == "UUURL"