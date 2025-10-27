# TinyURL — 生成 / 跳转 / 统计访问次数

## 问题描述

实现一个简化版 URL 短链接系统，支持以下功能：

1. `shorten(longUrl) -> shortCode`
   - 为给定的长链接生成一个**短码** `shortCode`（例如 6–8 位 Base62）。
   - 同一 `longUrl` 多次调用可返回同一短码或新的短码（和面试官约定即可）。
   - 要求短码**唯一**。
2. `redirect(shortCode) -> longUrl`
   - 根据 `shortCode` 返回原始 `longUrl`，用于跳转。
   - 同时把该短码的访问计数 `+1`。
3. `stats(shortCode) -> visits`
   - 返回该短码被访问的总次数。

> 允许只在内存中实现（无需持久化）。若短码不存在，返回错误。

## 数据结构（参考）

- `code_to_url: HashMap<string, string>`
- `url_to_code: HashMap<string, string>`（可选，用于同 URL 复用短码）
- `code_to_count: HashMap<string, int>`
- 短码生成：随机生成 Base62 字符串；若冲突，**重试**直到唯一。

## 函数签名（示例 / Python）

```python
class TinyURL:
    def shorten(self, longUrl: str) -> str: ...
    def redirect(self, shortCode: str) -> str: ...  # 同时计数 +1
    def stats(self, shortCode: str) -> int: ...
```

## 行为示例

```
tiny = TinyURL()
c1 = tiny.shorten("https://example.com/a/b/c")   # "f3K9aZ"
c2 = tiny.shorten("https://example.com/d")       # "hQ12Lm"

tiny.redirect("f3K9aZ")  # -> "https://example.com/a/b/c"（计数+1）
tiny.redirect("f3K9aZ")  # -> 同上（计数再+1）
tiny.redirect("hQ12Lm")  # -> "https://example.com/d"

tiny.stats("f3K9aZ")     # -> 2
tiny.stats("hQ12Lm")     # -> 1
tiny.redirect("noSuch")  # -> 错误（404 / None / Exception）
```

## 复杂度

- `shorten`：均摊 `O(1)`（哈希 + 随机重试期望常数次）
- `redirect`：`O(1)`（查表 + 计数）
- `stats`：`O(1)`

## 细节与边界

- 短码字符集：`[A-Za-z0-9]`；长度 6–8（和面试官约定）。
- 冲突处理：随机生成 → 若 `code_to_url` 已有该码则重试。
- 可选：支持**自定义别名**、过期时间（TTL）、黑名单域名、速率限制等（非必需）。

------

## Follow-up：分布式环境下如何保证短码唯一？

可选方案（任一即可，面试官认可）：

1. **分布式 ID 生成器**（如 Snowflake / Sonyflake）：生成全局唯一 64 位 ID，再做 Base62 编码为短码。
2. **中心化原子计数器**（如 Redis `INCR`）：把单调递增的整数用 Base62 编码作为短码；`INCR` 保证**强一致唯一**。
3. **分片前缀 + 本地计数器**：为每台机器分配唯一前缀（机房ID/机器ID），本地自增计数拼接前缀，避免跨机锁；保证全局唯一。
4. 若仍用**随机码**：使用强一致的**去重存储**（如 Redis `SETNX` / 数据库唯一索引）在写入时原子校验，不通过则重试。

> 一致性与可用性权衡：读多写少的系统可用主从 + 缓存；热点短码可做缓存层（TTL）并异步回写计数（或使用 Redis `INCR` 做计数聚合）。