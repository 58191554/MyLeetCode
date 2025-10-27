# Restaurant Waiting List — 最小可容纳规则的叫号服务

## 问题描述

设计并实现一个餐厅等候系统 `WaitlistSystem`，系统维护若干**等候中的顾客团体**（`groupSize`），并支持当有空桌时按“**最小可容纳**”规则分配座位：

> 给定一张容量为 `tableSize` 的桌子，系统应找到**队列中第一个 `groupSize ≤ tableSize` 的顾客团体**进行入座；若存在多组满足条件，按**到达先后**（先到先服务）择优；若不存在，返回空（或保留桌子待用）。

可假设一个桌子一次只服务一个团体；团体一旦入座即从等候队列中移除。

## 功能需求

实现以下接口（语言自选，下面为 Python 示意）：

```python
class WaitlistSystem:
    def arrive(self, group_id: str, group_size: int) -> None:
        """顾客到达，加入等候队列；group_id 全局唯一。"""

    def cancel(self, group_id: str) -> bool:
        """顾客取消等候，若存在则从系统移除并返回 True，否则 False。"""

    def seat(self, table_size: int) -> str | None:
        """
        给定桌子容量，分配给等候队列中“第一个且 group_size ≤ table_size”的团体，
        并将其从系统中移除；返回 group_id。若没有可用团体，返回 None。
        """

    def size(self) -> int:
        """当前等候中的团体数量。"""
```

### 业务规则（默认约定）

- **到达顺序优先**：在所有 `group_size ≤ table_size` 的团体中，选**到达时间最早**的那一个。
- `group_size`、`table_size` 为正整数；`group_id` 唯一。
- `cancel` 可在任何时刻调用；被取消的团体不可再被分配。
- 不考虑拼桌与拆分（一个桌子只给一个团体）。

## 示例

```
S.arrive("g1", 2)
S.arrive("g2", 4)
S.arrive("g3", 2)

S.seat(2)  -> "g1"   # 可容纳(≤2)的中到达最早的
S.seat(3)  -> "g3"   # 现有候选是 g3(2)，g2(4不行)，取 g3
S.seat(4)  -> "g2"   # 只剩 g2(4)
S.seat(2)  -> None   # 空
```

## 目标与约束

- 操作规模：`N` 可达 `1e5 ~ 1e6`。
- 需要在**在线**场景下高效支持 `arrive / cancel / seat` 的混合调用。
- 时间复杂度目标（两种实现路线）：
  - **基础版（易实现）**：
    - 维护两层结构：
      1. 全局到达顺序队列（或双端队列）保存`group_id`顺序；
      2. 以 `group_size` 为键的**有序列表**或**哈希桶**（如 `size -> 队列`），`seat(table)`时从 `size = 1..table_size` 顺序查找第一个非空桶，并在桶内按到达顺序取队首。
    - 复杂度：`arrive O(1)`，`cancel O(1)`（哈希定位并标记失效），`seat` 最坏 `O(table_size)` 或 `O(maxSize)`；可通过维护**Fenwick/Segment Tree**上的“桶是否非空”的位来把 `seat` 降到 `O(log M)`（`M` 为最大支持的 `group_size`）。
  - **优化版（面试可直接“假设有平衡树”）**：
    - 用**平衡二叉搜索树**或**有序映射**（如 `TreeMap` / `std::map` / `SortedDict`）将 `group_size` 映射到“到达顺序队列”；
    - `seat(table)`：在有序结构上做 `floor(table)`（或 `upper_bound(table)` 取不大于 `table` 的最大键），若该桶非空则弹出队首；若为空向更小键继续（可用树内自带的前驱操作）。
    - 复杂度：`arrive O(log M)`，`cancel O(log M)`（通过 `group_id` 定位其桶并在队列中 O(1) 删除/惰性删除），`seat O(log M)`。
- 空间复杂度：`O(N)`。

## 数据结构建议

- **索引**：`id -> (group_size, node_handle)` 方便 `cancel` O(1)/O(log M) 定位与删除；`node_handle` 可是链表节点指针或队列迭代器。
- **桶**：`size -> deque<group_id>`，保持到达顺序。
- **有序索引**（优化版）：平衡树维护**非空桶的键集合**；或在 Fenwick/Segment Tree 上把“桶是否为空”视为 `0/1`，支持“≤ table_size 的最大非空桶”的查询。

## 边界与异常

- 重复 `group_id` 到达：抛错或忽略（需在题面明确；默认抛错）。
- `cancel` 不存在的 `group_id`：返回 `False`。
- `table_size` 小于所有等候 `group_size`：`seat` 返回 `None`。
- 若需要支持**多桌一次性分配**，可将 `seat_many([t1,t2,...])` 作为扩展。

## 可选扩展（Follow-ups）

1. **并发场景**：读写锁或基于队列/树的细粒度锁；高并发下考虑无锁队列 + 原子标记惰性删除，后台清理。
2. **优先级**：支持会员/预约优先，可在桶内改为**稳定的多级队列**（`priority -> deque`），或在树键中加入复合键 `(group_size, -priority)`。
3. **动态统计**：支持查询当前可服务的最小桌子尺寸、平均等待时间、各 `group_size` 的人数等。
4. **上界未知的 group_size**：若 `group_size` 无上界，Fenwick/线段树不适合，优选“平衡树 + 非空桶”方案。
5. **分区/多门店**：按门店/区域分片，每片维护独立结构，上层做路由与聚合。

------

如果你需要，我可以按你偏好的语言给出**基础版（桶 + deque）**与**优化版（有序映射 + 前驱查询）**的参考代码模板，并标出可直接替换为“已实现的 balanced search tree”的接口。