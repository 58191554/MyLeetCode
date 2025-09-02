# 逐步设计题：可复用的泛型 Key-Value Store（带命中统计 & 并发安全）

这是一道**循序渐进**的系统/代码设计题。面试官会分轮提出需求，请你在每一轮**明确做出设计决策（decision）**并写出**高质量代码**。在每轮结束时，需简短说明你的取舍（例如：复杂度、可维护性、扩展性、并发语义、错误处理等）。

---

## Round 1 —— 设计一个泛型 Key-Value Store

**目标**：实现一个内存型 KV 存储，支持泛型键值，关注“用户体验”。

### 要求

* 语言建议：Java（也可用 Go/TS，但需体现泛型/约束）。
* 接口（可自行调整命名，允许增加方法）：

  ```java
  public interface KeyValueStore<K, V> {
      V get(K key);                  // 若不存在，返回 null 或抛出受检异常 —— 需说明你的选择
      void put(K key, V value);      // 不允许 null? 若允许需定义语义
      V remove(K key);               // 返回被移除的旧值或 null
      boolean containsKey(K key);
      int size();
      void clear();
  }
  ```
* 复杂度：常见操作 **期望 O(1) 均摊**。
* 可用性（“用户体验”）：

  * 约束与错误信息清晰（例如：key/value 为空的行为；不存在键时 get 的语义；异常 vs 特殊返回值）。
  * 文档/注释与单元测试覆盖常见边界（空 store、覆盖写入、移除不存在键等）。
* 设计决策说明（必写）：

  * 为什么选择 `null` 返回 vs 抛异常？
  * 对 `K` 的约束（可变性、`equals/hashCode`、比较器）。
  * 扩容策略/数据结构选择（例如 `HashMap` vs 开放寻址等）。

---

## Round 2 —— 支持“命中次数（Hit Count）”功能

**目标**：在不改变 Round 1 使用体验的前提下，统计**每个 key 被成功 `get` 的次数**。

### 要求

* **命中定义**：仅当 `get(key)` 找到且返回非空（或未抛出“未找到”异常）时计一次命中。
* 新接口（可装饰/扩展）：

  ```java
  public interface HitCountReadable<K> {
      long getHitCount(K key);           // 返回该 key 的累计命中数（不存在则为 0）
      Map<K, Long> topHits(int k);       // 返回命中数 Top-k（k<=size），要求有序（命中数降序，命同则按 key 顺序）
      long getTotalHits();               // 全局命中次数
  }
  ```
* 行为语义需清晰说明：

  * `get(key)` 未命中是否影响统计？（通常不计）
  * `remove/clear` 对命中统计是否重置？（由你定义，但要解释理由）
* 性能要求：

  * `getHitCount`、`getTotalHits` **O(1)**；
  * `topHits(k)` 允许 **O(n log k)**。
* 设计决策说明（必写）：

  * 将命中统计与存储解耦还是内联？（见 Round 3）
  * 命中计数的溢出语义（`long` 溢出如何处理）。

---

## Round 3 —— 为“可复用性（Reusability）”重构

**目标**：让“命中统计”可复用到**任意** `KeyValueStore` 实现，而无需改底层存储代码。

### 要求

* 推荐使用**装饰器模式（Decorator）**或**组合**：

  ```java
  public final class HitCountingStore<K, V>
      implements KeyValueStore<K, V>, HitCountReadable<K> {

      private final KeyValueStore<K, V> delegate;
      // 命中计数存储：如 ConcurrentHashMap<K, AtomicLong>（并发语义见 Round 4）
  }
  ```
* 复用目标：

  * 你的 `HitCountingStore` 应能包裹任何实现了 `KeyValueStore<K,V>` 的实例（例如将来切换到 LRU、带 TTL 的实现）。
* API 稳定：**不改变** Round 1 的调用方式。
* 设计决策说明（必写）：

  * 为什么选择装饰器而非继承？
  * 如何避免计数逻辑“泄漏”到业务层？
  * 如何保证 `topHits(k)` 的可扩展性（数据结构、接口返回有序 Map 的选择与理由）。

---

## Round 4 —— 并发与 Race Condition

**目标**：识别并修复竞态条件，给出线程安全的实现与测试。

### 需要考虑的典型竞态

* **读写并发**：`put/remove/clear` 与并发 `get`/命中计数。
* **计数丢失**：两个线程同时 `get(key)`，命中数自增是否丢失？
* **检查-后-执行**：`if (!map.containsKey(k)) put(k,v)` 的 ABA 问题。
* **可见性**：写入后的值与命中数对其他线程是否可见。

### 要求

* 指定并发语义（文档化）：

  * 是否提供**线性化**的 `get/put/remove`？
  * 命中计数的**至少-一次** vs **恰好-一次**保证（推荐“恰好一次”，即每次成功 get 必增 1）。
* 技术路线（任选并说明理由）：

  * `ConcurrentHashMap` + `AtomicLong`（自增用 `incrementAndGet()`；`computeIfAbsent` 避免竞态初始化）。
  * 读写锁（`ReentrantReadWriteLock`）或分段锁/条带化。
  * 不建议整个 store 粗粒度 `synchronized`（说明权衡）。
* 测试要求

  * 多线程压力测试：N 线程对同一 key 做大量 `get`，命中数应等于成功 `get` 次数之和。
  * 交错操作：并发 `put/remove/clear` 与 `get/topHits`，验证不抛异常、语义一致。
* 设计决策说明（必写）：

  * 你如何证明没有**丢计数**？
  * `topHits(k)` 在并发下的一致性级别（快照一致/最终一致），为什么？

---

## 约束 & 评分点

* **可读性**：清晰的接口、注释、异常语义与边界行为说明。
* **决策说明**：每轮结束提供 ≤200 字的 Design Notes，陈述取舍与替代方案。
* **复杂度**：核心操作 O(1) 均摊，`topHits` 不苛求全局最优但要合理。
* **可复用性**：命中统计作为可插拔特性，无需改动底层 store。
* **并发安全**：无明显竞态；对并发语义有清晰、可测试的定义。
* **测试**：覆盖空/缺失 key、大量命中、并发交错、清理后的行为。

---

## 示例交互（Java 伪代码）

```java
KeyValueStore<String, Integer> base = new InMemoryHashMapStore<>();
KeyValueStore<String, Integer> store =
    new HitCountingStore<>(base); // 装饰器添加命中统计

store.put("a", 42);
store.get("a");  // 命中+1
store.get("a");  // 命中+1
((HitCountReadable<String>) store).getHitCount("a"); // => 2

store.remove("a");
boolean hasA = store.containsKey("a"); // => false
// remove 后命中是否保留？请在文档中定义并实现
```

并发测试要点（示例）：

* 10 个线程并发执行 10\_000 次 `get("hot")`（确保 key 已存在），最终 `getHitCount("hot") == 100_000`。
* 并发 `put/remove/clear` 期间 `get` 不抛出未定义异常；若语义允许瞬时未命中，命中数仅对成功 `get` 计数。

---

## 可选加分项（不要影响主线）

* 支持 **Top-k** 的增量维护（小根堆/跳表）以降低 `topHits(k)` 开销。
* 指标导出（如 Micrometer 接口），或事件流（`StoreEventListener`）用于不同特性解耦。
* TTL/LRU 存储实现，并证明装饰器的可插拔性。
* 简易基准（JMH）对比不同并发策略的吞吐/延迟。

---

> 交付物清单
>
> 1. 代码（Round 1–4），2) 设计说明（每轮 ≤200 字），3) 单元/并发测试，4) README（构建/运行方式与并发语义）。
