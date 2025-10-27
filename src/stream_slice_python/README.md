# Stream Slice — Return First *n* or Last *n* Elements of a Stream

## Problem

实现一个流数据处理函数 `stream_slice(stream, n)`：

- 若 `n > 0`：返回**前 `n` 个**元素（若流长度小于 `n`，则返回**全部**元素）。
- 若 `n < 0`：返回**最后 `|n|` 个**元素（若流长度小于 `|n|`，则返回**全部**元素）。
- 若 `n = 0`：返回空结果。

> 这里的“流（stream）”指可**逐个读取**的序列（如迭代器/生成器/文件行流），不能随机访问，也不一次性加载全部数据。

## Function Signature（示例）

- Python

  ```python
  from typing import Iterable, Iterator, List, TypeVar
  T = TypeVar("T")
  
  def stream_slice(stream: Iterable[T] | Iterator[T], n: int) -> list[T]: ...
  ```

- 其他语言可用等价签名；要求**单次遍历**、时间 `O(L)`，其中 `L` 为流长度。

## Behavior Examples

### Example 1 — `n` 为正：取前 `n`

```
stream = [10, 20, 30, 40, 50]
n = 3
output = [10, 20, 30]
```

### Example 2 — `n` 为负：取最后 `|n|`

```
stream = [a, b, c, d, e]
n = -2
output = [d, e]
```

### Example 3 — 流长度不足

```
stream = [1, 2]
n = 5   -> output = [1, 2]
n = -5  -> output = [1, 2]
```

### Example 4 — `n = 0`

```
stream = any
n = 0   -> output = []
```

## Constraints & Requirements

- 仅允许**一次**线性扫描（不能多次遍历流）。
- 空间复杂度：
  - `n > 0`：`O(min(n, L))`（保存前 `n` 个或更少）。
  - `n < 0`：应使用**固定大小为 `|n|` 的滑动窗口**，空间 `O(min(|n|, L))`。
- 流可能非常大（甚至无限）；不应把整个流载入内存。

## Edge Cases / Clarifications

- 流可能为空：返回 `[]`。
- 元素类型任意且不需要可比较。
- 若输入的是迭代器，函数应**消费**它（之后迭代器可能已耗尽）。
- 允许 `n` 的绝对值大于流长度（如上例所示）。

## Follow-up（内存优化）

当 `n < 0` 且流极大时，如何减少内存占用？

- 使用**固定容量为 `|n|` 的循环数组/环形缓冲区（ring buffer）**作为滑动窗口：
   在扫描过程中不断覆盖最旧元素，仅保留最近的 `|n|` 个。最终按正确顺序输出缓冲内容。
- 该方案将空间从 `O(L)` 降至 `O(|n|)`，满足内存约束。

------

需要代码模板或环形缓冲区的最小实现，我也可以直接给你一版（Python/C++/Java 任一）。