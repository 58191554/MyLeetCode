这题最接近的力扣题是：

- **LeetCode 527. Word Abbreviation**（付费题，要求为一组单词生成**互不冲突**的最短缩写）
- 相关题：**LeetCode 288. Unique Word Abbreviation**（设计结构判断某缩写在字典中是否唯一）、**LeetCode 408. Valid Word Abbreviation**（校验缩写是否匹配单词）

下面给你一份可直接用于面试/作业的正式题面（对应 527 的生成版，并体现你说的“prefix + omitted count + suffix”格式与唯一性要求）。

# Unique String Compression / Abbreviation

## 问题描述

给定一组不为空、仅包含小写字母的字符串 `words`。为每个单词生成一个**缩写**，格式为：

```
abbr = prefix + omitted_count + last_char
```

- `prefix`：单词的前缀，长度 ≥ 1
- `omitted_count`：中间被省略的字符数量（十进制，无前导 0；若为 0 则可省略该数字）
- `last_char`：单词最后一个字符

要求：

1. 对于输入中的每个单词，生成一个**唯一**的缩写（不同单词的缩写不能相同）。
2. **尽量短**：在满足唯一性的前提下，缩写应尽可能短（通常按缩写字符串长度最小为目标；若长度相同，任何一种都可）。
3. 单词长度 ≤ 2 时，缩写通常等于原词（因为无法形成更短且带数字的形式）。

**函数签名（示例 / Python）**

```python
from typing import List
def abbreviate_unique(words: List[str]) -> List[str]:
    ...
```

## 示例

```
输入:
["like","god","internal","me","internet","interval","intension","face","intrusion"]

一种合法输出:
["l2e","god","internal","me","i6t","interval","inte4n","f2e","intr4n"]

解释：
- "like" → "l2e"
- "internal" 与 "interval" 首字母相同、末字母相同且长度相同，初始都会生成 "i6l"/"i6l" 冲突；
  需增加前缀长度逐步消解冲突，得到 "internal"（无法更短）与 "interval"。
- "internet" 与 "intension"/"intrusion" 也需要按前缀扩展至唯一。
```

## 约束（可与面试官确认）

- `1 ≤ len(words) ≤ 10^5`
- 每个单词仅含小写字母，`1 ≤ |word| ≤ 400`
- 期望时间复杂度：`O(n log n)` 或 `O(n · L)`（`L` 为均值长度），空间 `O(n)`

## 期望思路（与你的思路一致）

1. **初始缩写**：对每个词生成 `p=1` 的缩写：`word[0] + (len-2) + word[-1]`；若 `len ≤ 3`，一般不缩写。
2. **按冲突分组**：把产生相同缩写的词放到同一组。
3. **逐步增加前缀长度**：对每个冲突组，增加这些词的前缀长度 `p`（可用**字典树 / 前缀计数**或哈希），直到组内各词缩写唯一。
   - 常见实现：对同一组按原词排序，计算相邻词的**最长公共前缀**（LCP），令每个词的 `p = max(1, LCP_with_prev, LCP_with_next) + 1`，再据此形成缩写；若仍冲突，继续扩展。
4. **唯一性维护**：用哈希表记录已生成的缩写；若冲突，扩前缀或直接退回原词。

**复杂度**：分组 + LCP/前缀扩展可做到近似 `O(n · L)`；用 Trie 也可，但实现复杂些。

## Follow-up（分布式 / 全局唯一）

- 多机生成时，需保证全局唯一：
  - 先按**长度、首字母、末字母**分桶，同桶内再做前缀扩展；
  - 用集中式冲突检测（如 Redis/DB 唯一约束）或分区一致性哈希；
  - 若仍冲突，可**增加前缀长度**或在中间数后附加**稳定标识**（如分区号）。

------

若你需要，我可以补充一份 Python 参考实现：基于“同长度+首尾字符分组 + LCP 计算 + 逐步扩大前缀”的做法，能通过 527 的典型数据规模。