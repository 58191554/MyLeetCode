下面是一份可直接用于面试/笔试的「正式题面」，含定义、输入输出、示例与进阶要求。

# Number of Islands in a Binary Tree

## Problem

给定一棵二叉树，每个结点的值为 `0` 或 `1`。**岛屿（island）**定义为：在该树的无向视图中，由值为 `1` 的结点组成的**极大连通分量**（连通性仅通过父子边）。求树中岛屿的个数。

更直观地说：把整棵树当作无向图；相邻定义为父子相邻。若一组 `1` 结点之间两两可通过仅由 `1` 结点组成的路径连通，且无法再加入更多 `1` 结点，便构成一个岛屿。要求返回岛屿的数量。

## Follow-up

返回**每个岛屿的大小**（岛屿包含的 `1` 结点数）。输出顺序不限。
（如需要“去重的岛屿大小集合”，可对结果去重并排序，但**默认**返回所有岛屿的大小列表。）

## Input

* 一棵二叉树的根结点 `root`。
  结点结构：

  ```
  class TreeNode {
      int val;       // 0 or 1
      TreeNode left;
      TreeNode right;
  }
  ```

## Output

* 基础：返回一个整数 `count`，表示岛屿数量。
* 进阶：返回一个整数数组 `sizes`，表示每个岛屿的大小（元素个数即为 `count`）。

## Constraints

* 树中结点数 `1 <= n <= 2 * 10^5`（面试时可根据语言/平台调整）
* 结点值仅为 `0` 或 `1`
* 允许树退化为链、允许全部为 `0` 或全部为 `1`

## Examples

### Example 1

```
Input tree (level order): [1,1,0,1,0,null,1]
           1
         /   \
        1     0
       /       \
      1         1

Islands: { (root-left-left)-(root-left)-(root) } 和 { (right-right) }
Output (count): 2
Output (sizes): [3, 1]   // 顺序不限
```

### Example 2

```
Input: [0,0,0]
All zeros → no island
Output (count): 0
Output (sizes): []
```

### Example 3

```
Input: [1,null,1,null,1]
A right-leaning chain of 1s → single island of size 3
Output (count): 1
Output (sizes): [3]
```

## Required / Expected Solution

* 一次 DFS/BFS 遍历整棵树，遇到尚未访问的值为 `1` 的结点即启动一次连通分量搜索，统计该分量大小；计数 `+1`，并把大小加入 `sizes`。
* 时间复杂度 `O(n)`；空间复杂度 `O(h)`（递归栈，`h` 为树高；或使用显式栈/队列 `O(n)` 最坏）。

## Function Signatures (任选其一说明即可)

**Java**

```java
int countIslands(TreeNode root);

List<Integer> islandSizes(TreeNode root); // follow-up
```

**Python**

```python
def count_islands(root: Optional[TreeNode]) -> int: ...
def island_sizes(root: Optional[TreeNode]) -> list[int]: ...
```

**C++**

```cpp
int countIslands(TreeNode* root);
std::vector<int> islandSizes(TreeNode* root); // follow-up
```

## Edge Cases to Clarify (默认约定已给出)

* 父子连通仅通过**父子边**（不考虑“兄弟相邻”等其他邻接）。
* 路径中的所有结点必须为 `1` 才能将两个 `1` 结点视为同一岛屿。
* Follow-up 默认返回**所有岛屿的大小列表**；若题目要求“unique sizes”，对该列表去重即可。
