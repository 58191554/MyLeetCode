from typing import List, Optional
import random

class Solution:
    # ------- Treap 结点 -------
    class Node:
        __slots__ = ("s", "e", "prio", "l", "r", "sum")
        def __init__(self, s: int, e: int):
            self.s = s
            self.e = e
            self.prio = random.randrange(1 << 30)
            self.l: Optional["Solution.Node"] = None
            self.r: Optional["Solution.Node"] = None
            self.sum = e - s  # 子树总点数，初始为自身长度

    # ------- Treap 工具函数 -------
    @staticmethod
    def _len(n: Optional["Node"]) -> int:
        return 0 if n is None else (n.e - n.s)

    @staticmethod
    def _sum(n: Optional["Node"]) -> int:
        return 0 if n is None else n.sum

    @classmethod
    def _recalc(cls, n: Optional["Node"]) -> None:
        if n is not None:
            n.sum = cls._sum(n.l) + (n.e - n.s) + cls._sum(n.r)

    @classmethod
    def _merge(cls, a: Optional["Node"], b: Optional["Node"]) -> Optional["Node"]:
        if not a or not b:
            return a or b
        if a.prio < b.prio:
            a.r = cls._merge(a.r, b)
            cls._recalc(a)
            return a
        else:
            b.l = cls._merge(a, b.l)
            cls._recalc(b)
            return b

    @classmethod
    def _make_node(cls, s: int, e: int) -> Optional["Node"]:
        if e <= s:
            return None
        return Solution.Node(s, e)

    @classmethod
    def _split_by_points(cls, n: Optional["Node"], k: int) -> (Optional["Node"], Optional["Node"]):
        """
        把 n 切成 (A, B)，使得 A 覆盖前 k 个点，B 覆盖剩余点（保持原有先后顺序）
        0 <= k <= sum(n)
        """
        if n is None:
            return None, None
        left_sum = cls._sum(n.l)
        cur_len = n.e - n.s

        if k <= left_sum:
            a, new_left = cls._split_by_points(n.l, k)
            n.l = new_left
            cls._recalc(n)
            return a, n
        elif k >= left_sum + cur_len:
            new_right, b = cls._split_by_points(n.r, k - left_sum - cur_len)
            n.r = new_right
            cls._recalc(n)
            return n, b
        else:
            # 切在当前结点内部：把 [s,e) 在 t 处分裂为 [s,t) 和 [t,e)
            t = n.s + (k - left_sum)
            left_node = cls._make_node(n.s, t)   # 必然非空
            right_node = cls._make_node(t, n.e)  # 必然非空
            # 左树 = merge(n.l, left_node), 右树 = merge(right_node, n.r)
            left_tree = cls._merge(n.l, left_node)
            right_tree = cls._merge(right_node, n.r)
            # 丢弃 n（原结点已被两半替代）
            return left_tree, right_tree

    @classmethod
    def _build(cls, intervals: List[List[int]]) -> Optional["Node"]:
        root = None
        for s, e in intervals:
            node = cls._make_node(s, e)
            if node:
                root = cls._merge(root, node)
        return root

    @classmethod
    def _inorder(cls, n: Optional["Node"], out: List[List[int]]) -> None:
        if not n:
            return
        cls._inorder(n.l, out)
        out.append([n.s, n.e])
        cls._inorder(n.r, out)

    # ------- 对外接口：多次删除 -------
    def deleteCoveredPoint(self, intervals: List[List[int]], ops: List[int]) -> List[List[int]]:
        root = self._build(intervals)
        total = self._sum(root)

        for k in ops:
            if k < 0 or k >= total:
                raise IndexError(f"delete index {k} out of range 0..{total-1}")
            # A 吃掉前 k 个点，B 含目标点在首位
            A, B = self._split_by_points(root, k)
            # mid 是长度为 1 的单点段，把它丢弃；C 是剩余
            mid, C = self._split_by_points(B, 1)
            # mid 被 GC 回收；合并 A 与 C
            root = self._merge(A, C)
            total -= 1

        ans: List[List[int]] = []
        self._inorder(root, ans)
        return ans
