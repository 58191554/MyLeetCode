"""
https://stackoverflow.com/questions/76142856/finding-a-path-between-two-nodes-in-a-k-th-order-fibonacci-tree
"""


class TreeNode:
    def __init__(self, val, order):
        self.l = None
        self.r = None
        self.val = val
        self.order = order


class Solution:
    def find_fib_path(self, start_label: int, end_label: int, root: TreeNode) -> str:
        # Handle trivial case
        if start_label == end_label:
            return ""

        # Compute subtree sizes: size(n) = size(n-2) + size(n-1) + 1 with size(0)=size(1)=1
        size_cache = {0: 1, 1: 1}

        def tree_size(order: int) -> int:
            if order in size_cache:
                return size_cache[order]
            size_cache[order] = tree_size(order - 2) + tree_size(order - 1) + 1
            return size_cache[order]

        # Compute path from root (label 0) to a given target label using only L/R
        def path_from_root_to_label(order: int, root_label: int, target_label: int) -> str:
            if target_label == root_label:
                return ""
            if order <= 1:
                # Leaf but different label -> invalid
                raise ValueError("Target label not present in the tree of given order")

            left_size = tree_size(order - 2)
            left_start_label = root_label + 1
            left_end_label = root_label + left_size

            if target_label <= left_end_label:
                return "L" + path_from_root_to_label(order - 2, left_start_label, target_label)

            right_start_label = left_end_label + 1
            return "R" + path_from_root_to_label(order - 1, right_start_label, target_label)

        order = root.order
        path_root_to_start = path_from_root_to_label(order, 0, start_label)
        path_root_to_end = path_from_root_to_label(order, 0, end_label)

        # Find longest common prefix (LCA)
        common = 0
        for a, b in zip(path_root_to_start, path_root_to_end):
            if a == b:
                common += 1
            else:
                break

        ups = len(path_root_to_start) - common
        downs = path_root_to_end[common:]
        return ("U" * ups) + downs 
        

            