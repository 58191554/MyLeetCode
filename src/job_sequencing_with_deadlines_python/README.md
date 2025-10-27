# Job Sequencing with Deadlines — 输出按时间顺序的最大奖励计划

## 问题描述

给定一批任务，每个任务包含：

- `id`：任务唯一标识
- `deadline`：该任务必须在不晚于此时间槽（slot）执行（每个任务耗时恰为 1 个时间槽）
- `reward`：完成该任务可获得的奖励

在满足**每个时间槽最多执行一个任务**、且**每个任务最迟在其 `deadline` 前完成**的前提下，选择一部分任务执行，使**总奖励最大化**。请输出：

1. 最大总奖励；
2. 选中任务按**实际执行时间从早到晚**的顺序（即时间槽顺序）的任务 `id` 列表。

> 时间槽是离散的正整数：`1, 2, 3, ...`。若任务 `deadline = d`，则该任务只能被安排在某个 `t`，满足 `1 ≤ t ≤ d`。

## 函数签名（示例）

**Python**

```python
from typing import List, Tuple
class Task(Tuple[int, int, int]): ...  # or a dataclass (id, deadline, reward)

def schedule_jobs(tasks: List[Tuple[int, int, int]]) -> Tuple[int, List[int]]:
    """
    :param tasks: 列表中的每个元素为 (id, deadline, reward)
    :return: (max_reward, order_by_time)
    """
```

## 约束（可与面试官确认；默认建议）

- 任务数 `1 ≤ n ≤ 2 * 10^5`
- `1 ≤ deadline ≤ 2 * 10^5`
- `-10^9 ≤ reward ≤ 10^9`（通常为非负；若允许负值，可直接跳过负奖励任务）
- 可用内存与时间需适配 `n log n` 级别算法

## 示例

输入：

```
tasks = [
  (A, 2, 100),
  (B, 1, 19),
  (C, 2, 27),
  (D, 1, 25),
  (E, 3, 15)
]
```

一种最优安排：

- 时间槽 1：任务 D（奖励 25）
- 时间槽 2：任务 A（奖励 100）
- 时间槽 3：任务 E（奖励 15）

输出：

```
max_reward = 140
order_by_time = [D, A, E]   # 按时间槽从早到晚
```

## 期望思路（贪心 + 反向找空槽）

1. 按 `reward` 从高到低排序任务；
2. 对每个任务，尝试把它放进**不晚于其 `deadline` 的最靠后**的空时间槽：
   - 若找到空槽 `t`（`1 ≤ t ≤ deadline`），占用它并计入奖励；
   - 若找不到空槽，则跳过此任务。
3. 最终将占用的时间槽按 `t=1..T` 输出对应的任务 `id`，即为按时间先后的执行顺序。

实现上可用：

- **并查集 / 领接表（DSU）**：`find(t)` 返回 `≤ t` 的最新空槽；安放到 `slot = find(deadline)` 后，将该槽与 `slot-1` 合并。
  - 复杂度：排序 `O(n log n)` + 每次 `find/union` 近似 `α(n)`，总计 `O(n log n)`。
- 或用**布尔数组从后往前扫描**寻找空位（最坏 `O(n^2)`，不推荐在大输入）。

## 输出与细节约定

- 若存在多个最优解，返回任意一个即可（除非面试官要求特定 tie-break）。
- 若需要稳定性（相同奖励时优先较小 `deadline` 或较小 `id`），请在排序时明确 tie-break 规则。
- 若所有任务 `deadline` 很大，可将最大考虑到的时间槽限制为 `max_deadline = max(deadline_i)`，无需开更大的结构。

## 复杂度目标

- 时间：`O(n log n)`（排序主导）
- 空间：`O(max_deadline)` 用于并查集或槽位数组

------

需要的话，我可以提供**并查集版本**或**数组版本**的参考实现（Python/C++/Java 任一），并附带将占用槽位恢复为按时间顺序的 `id` 列表。