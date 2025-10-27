# Diameter of a Binary Tree（按“边数”计）

## Problem

给定一棵二叉树，**直径（diameter）\**定义为树中任意两结点之间路径所经过的\**边数**的最大值。请实现函数返回该直径。

> 注意：直径按**边数**计数，而非结点数。空树与单结点树的直径为 0。

### 结点定义（示例）

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val  = val
        self.left = left
        self.right= right
```

## Function Signature

- Python

  ```python
  def diameter_of_binary_tree(root: TreeNode | None) -> int: ...
  ```

## Constraints

- 结点数 `0 <= n <= 2 * 10^5`
- 允许退化为链
- 期望时间复杂度 `O(n)`，额外空间（递归栈） `O(h)`，其中 `h` 为树高

## Explanation / Hint

对每个结点：

- 令 `depth(node)` 为该结点到其**最深叶子**的边数；
- 经过该结点的最长路径长度为 `left_depth + right_depth`（两条向下路径拼接）；
- 在递归计算 `depth` 时，用全局/外部变量维护直径最大值；
- 函数向父结点返回 `max(left_depth, right_depth) + 1`。

## Examples

### Example 1

输入（层序）：

```
[1, 2, 3, 4, 5]
        1
      /   \
     2     3
    / \
   4   5
```

解释：最长路径为 `4-2-5` 或 `4-2-1-3`（边数分别为 2 和 3），最大为 3。
 输出：

```
diameter = 3
```

### Example 2

```
[1]  -> diameter = 0
[]   -> diameter = 0
```

------

## Follow-up: N 叉树（多叉树）

若每个结点可有任意数量的子结点（N 叉树），直径定义同上（任意两点之间的最大边数）。
 思路：对每个结点，收集其所有子树深度，取**最大的两个**深度 `d1 >= d2`，用 `d1 + d2` 更新全局直径；向父结点返回 `max_depth + 1`。

- 时间复杂度 `O(n)`；空间复杂度 `O(h)`。

### N 叉树结点（示例）

```python
class Node:
    def __init__(self, val=0, children=None):
        self.val = val
        self.children = children or []
```

------

\##（可选）参考调用示例

```python
# 构造 Example 1
n4 = TreeNode(4); n5 = TreeNode(5)
n2 = TreeNode(2, n4, n5); n3 = TreeNode(3)
root = TreeNode(1, n2, n3)

assert diameter_of_binary_tree(root) == 3
assert diameter_of_binary_tree(TreeNode(1)) == 0
assert diameter_of_binary_tree(None) == 0
```

> 常见陷阱：把“直径按结点数”与“按边数”混淆；只返回单侧深度而忘了用“两侧深度之和”更新答案；深链导致递归过深（必要时改迭代或调大递归限）。