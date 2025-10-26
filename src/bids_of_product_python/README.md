下面给你一份“面试版题面”，把需求、接口、约束、返回与细节都说清楚（可直接给面试官看/抄到题库里）。

# Implement Bids of Products

实现一个竞价管理数据结构，支持以下操作：

- `addBid(bid_id, product_id, price)`
   向系统加入一条出价。
   要求：`bid_id` 全局唯一；若 `bid_id` 已存在则更新其 `product_id` 与 `price`（等价于先删除旧的再添加新的）。
- `removeBid(bid_id) -> bool`
   从系统移除该 `bid_id` 对应的出价。若不存在返回 `false`，否则移除并返回 `true`。
- `queryClosestBid(product_id, price) -> (bid_id, price)`
   在 **指定商品** 的所有出价中，返回**价格最接近**给定 `price` 的那条出价。
   若有多条与 `price` 的差值相同，按以下规则打破平局：
  1. 价格较小者优先；
  2. 若价格也相同，则 `bid_id` 较小者优先。
      若该商品没有任何出价，返回空（或 `(-1, -1)`，由语言约定）。

## 说明

- 价格与 ID 为整数：
   `-10^9 <= price <= 10^9`，`1 <= bid_id, product_id <= 10^9`。
- 初始系统为空。
- 你需要设计 **近似在线** 的高效实现，目标复杂度：
  - `addBid / removeBid / queryClosestBid` 平均或最坏 **O(log n)**；
  - 额外空间 **O(n)**，其中 `n` 是系统中当前出价条数。
- `queryClosestBid` 仅在指定 `product_id` 的集合里比较“最接近”。

## 函数签名（任选其一实现）

- **Python**

  ```python
  class Bids:
      def addBid(self, bid_id: int, product_id: int, price: int) -> None: ...
      def removeBid(self, bid_id: int) -> bool: ...
      def queryClosestBid(self, product_id: int, price: int) -> tuple[int, int] | None: ...
  ```

## 示例

```
操作： 
addBid(101, 7, 500)
addBid(102, 7, 520)
addBid(103, 7, 480)
addBid(201, 8, 1000)

queryClosestBid(7, 510)  -> (102, 520)   // 差值：|520-510|=10，|500-510|=10，|480-510|=30；
                                         // 平局取更小价格与 510 同差的 500，但规则 1 说“价格更小优先”，
                                         // 注意这里与谁更接近：500 与 520 都差 10，先比价格小 => 返回 (101, 500)
```

> 按上面的平局规则，`queryClosestBid(7, 510)` **应返回 (101, 500)**。如果你想优先“更高价”或“更早插入”的，也可以在题面中改掉平局规则，但必须固定且清晰。

再举一组：

```
当前： product 9 有出价 (301, 300), (302, 400)
queryClosestBid(9, 350) -> (301, 300)    // |300-350|=50, |400-350|=50，平局取较小价格 => 300
removeBid(301)         -> true
queryClosestBid(9, 350) -> (302, 400)
removeBid(999)         -> false          // 不存在
```

## 边界与细则

- **更新语义**：若同一 `bid_id` 再次 `addBid`，视为更新（旧商品集合里删掉该条，再加入新商品集合）。
- **空集合**：某商品无出价时，`queryClosestBid` 返回空值（或 `(-1,-1)`）。
- **大量操作**：操作数可达 `2 * 10^5`。建议使用：
  - 全局 `unordered_map / HashMap`：`bid_id -> (product_id, price)`；
  - 每个 `product_id` 一个有序容器（如 `std::multiset<(price, bid_id)>` / `TreeMap<price, TreeSet<bidId>>`），
     以支持前驱/后继（floor/ceiling）查询做“最近价”。

## 进阶 Follow-ups（可选）

1. 支持 `queryKClosest(product_id, price, k)`。
2. 支持按时间或“活跃状态”打分的综合最近；或允许相同 `(product, price)` 出现多条时的返回策略。
3. 多线程并发读写如何做：分片锁/细粒度锁、读写锁、或无锁跳表。
4. 若内存受限，如何落盘（LSM-Tree 思路）并维持对“最近价”的低延迟查询。

——

需要的话，我可以按你偏好的语言写一份 **O(log n)** 的参考实现（含前驱/后继查询与更新语义）。