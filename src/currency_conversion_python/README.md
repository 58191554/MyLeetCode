# Currency Conversion — Max Product Path

## Problem

给定若干以字符串表示的汇率关系，每条关系形如：
`A:B:rate`，表示 **1 单位 A = rate 单位 B**。这些关系共同构成一张**有向图**（从 A 指向 B，权重为 `rate`）。

请实现一个函数，给定：

* 源货币 `src`
* 目标货币 `dst`
* 金额 `amt`（以 `src` 计价）

返回：将 `amt` 从 `src` 通过 **一条或多条中转路径** 转成 `dst` 能得到的**最大可能金额**。
若不存在任何可达路径，返回失败/抛错（或返回 `None`/`-1` 由你约定）。
若存在“无限放大”的情况（见下文“负权环 / 套利”），也应返回失败/抛错（或返回特殊标记）。

> 说明：最大金额 = 沿路径上各边汇率的**乘积** × `amt`；需在所有从 `src` 可达 `dst` 的路径中取最大乘积。

## Input Format

* `rates_str`: 形如
  `"USD:CAD:1.3, CAD:JPY:100, USD:GBP:0.8, GBP:JPY:150"`
  多个关系用逗号或空白分隔；注意这是一张**有向**图，只能按给定方向转换。
* `src`, `dst`: 字符串货币代码（大小写按输入对待，通常全大写）。
* `amt`: 浮点或整数，`amt ≥ 0`。

## Output

* 返回一个浮点数：最大可得到的 `dst` 金额（可四舍五入到所需小数位）。
* 若无路径，返回失败（抛异常/返回 `None`）。
* 若存在“无限可增加”的情况（套利环导致金额可无穷放大），返回失败（抛异常/返回特殊标记，如 `"INFINITE"`）。

## Examples

### Example 1（题面示例）

```
rates_str = "USD:CAD:1.3, CAD:JPY:100, USD:GBP:0.8, GBP:JPY:150"
query: convert(src="USD", dst="JPY", amt=10)
```

可选路径：

* 路径A：USD → CAD → JPY
  乘积 = 1.3 × 100 = 130
* 路径B：USD → GBP → JPY
  乘积 = 0.8 × 150 = 120

最大乘积 = 130 ⇒ 结果 = 10 × 130 = **1300 JPY**

**期望：** `convert(rates_str, "USD", "JPY", 10) = 1300.0`

### Example 2（不可达）

```
rates_str = "USD:CAD:1.3, CAD:JPY:100"
query: convert(src="JPY", dst="USD", amt=100)
```

图中没有从 `JPY` 到 `USD` 的有向路径。
**期望：** 返回失败（`None` / 抛异常）

### Example 3（套利/无限放大）

```
rates_str = "A:B:2, B:C:2, C:A:0.6"
# A→B→C→A 的乘积 = 2 * 2 * 0.6 = 2.4 > 1
query: convert(src="A", dst="C", amt=1)
```

存在乘积 > 1 的有向环（套利）。
这意味着你可以绕环多次再去 C，从而得到无限增加的金额（理论上无上界）。
**期望：** 返回失败/抛异常/特殊标记 `"INFINITE"`。

## Requirements / Hints

* **目标：** 找到 `src→dst` 的**最大乘积路径**。

* **两种主流做法：**

  1. **对数变换 + 最短路**：
     对每条边 `A→B (rate)` 令权重 `w = -log(rate)`。
     则最大乘积路径 ↔ 最小加权和路径。

     * 若存在负权环（即原图存在乘积 > 1 的环），则对应“可无限放大”情形。
     * 可用 **Bellman-Ford**：

       * 求最短路；
       * 检测从 `src` 可达且能影响到 `dst` 的负环（可在放松第 n 轮后从被更新的点做可达性筛选）。
     * 复杂度：`O(V*E)`，适合图不太大或需要严格环检测的场景。
  2. **直接在乘积域搜索**：

     * 以“当前可达的最大乘积”为距离，用最大堆（类似 Dijkstra 但改成“取最大”）；
     * 不处理环放大问题时更快（`O(E log V)`），但**不会**自动检测“乘积>1 的环”导致的无上界，需要额外处理（例如迭代次数/访问计数 + 逻辑判断，或结合对数+判环）。

* **边界情况：**

  * `src == dst`：通常返回 `amt`（或允许通过环放大时需要按负环规则处理）。
  * 大/小数率：建议计算中使用 `math.log` 与 `float`，并在输出时按业务规则舍入。
  * 输入解析：注意去除空格、大小写一致、重复边（可保留最大 rate）。

## Suggested Function Signatures

* Python

  ```python
  def convert(rates_str: str, src: str, dst: str, amt: float) -> float: ...
  ```
* 可选：同时返回路径

  ```python
  def convert_with_path(rates_str: str, src: str, dst: str, amt: float) -> tuple[float, list[str]]: ...
  ```

## Validation Snippets（调用示例）

```python
# Example 1
assert abs(convert("USD:CAD:1.3, CAD:JPY:100, USD:GBP:0.8, GBP:JPY:150",
                   "USD", "JPY", 10) - 1300.0) < 1e-6

# Example 2
assert convert("USD:CAD:1.3, CAD:JPY:100", "JPY", "USD", 100) is None  # 或捕获异常

# Example 3（应返回 'INFINITE' 或抛异常）
try:
    convert("A:B:2, B:C:2, C:A:0.6", "A", "C", 1)
    assert False, "should detect infinite arbitrage"
except InfiniteArbitrageError:
    pass
```

---

如果你想，我可以给出两版参考实现：

* **Bellman-Ford（带负环检测）**：安全、能识别套利；
* **最大堆的 Dijkstra 变体**：更快，但需自定义套利检测策略。
