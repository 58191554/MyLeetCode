from islands_in_a_binary_tree_python_ref import TreeNode, Solution
import pytest

def build_tree_level(arr):
    """
    Build binary tree from level-order list where None means no node.
    Example: [1, 0, 1, None, 1] 
    """
    if not arr:
        return None
    nodes = [None if v is None else TreeNode(v) for v in arr]
    i, n = 0, len(arr)
    for idx, node in enumerate(nodes):
        if node is None:
            continue
        li = 2*idx + 1
        ri = 2*idx + 2
        if li < n:
            node.left = nodes[li]
        if ri < n:
            node.right = nodes[ri]
    return nodes[0]

def test_example_mixed_two_islands():
    # Example-like: [1,1,0,1,None,None,1]
    #       1
    #     /   \
    #    1     0
    #   /       \
    #  1         1
    root = build_tree_level([1,1,0,1,None,None,1])
    assert Solution().numIslands(root) == 2

def test_all_zero():
    # [0,0,0] -> no island
    root = build_tree_level([0,0,0])
    assert Solution().numIslands(root) == 0

def test_right_chain_all_ones_single_island():
    # [1,None,1,None,1] (right-leaning chain of 1s) -> 1 island
    root = build_tree_level([1,None,1,None,1])
    assert Solution().numIslands(root) == 1

def test_siblings_ones_with_zero_parent_two_islands():
    # [0,1,1]  parent=0, two children=1 and 1 are NOT connected -> 2 islands
    root = build_tree_level([0,1,1])
    assert Solution().numIslands(root) == 2

def test_ones_separated_by_zero_should_be_two_islands():
    # 1 - right-> 0 - right-> 1  => 两个岛屿（被 0 隔开）
    # Level order: [1, None, 0, None, None, None, 1]
    root = build_tree_level([1, None, 0, None, None, None, 1])
    # 期望是 2；当前实现会错判为 1（暴露 Bug），如果你先修复再跑，应通过
    assert Solution().numIslands(root) == 2

@pytest.mark.parametrize(
    "arr, expected",
    [
        ([1], 1),               # single 1
        ([0], 0),               # single 0
        ([1,1,1], 1),           # full 1 small tree
        ([0,1,0,1,None,None,1], 2),  # 两个 1 子树彼此不连通
    ]
)
def test_parametrized(arr, expected):
    root = build_tree_level(arr)
    assert Solution().numIslands(root) == expected