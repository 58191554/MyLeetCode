package kv_store_java;

import java.util.*;
import java.util.NoSuchElementException;

/**
 * 装饰器：在不修改底层实现的前提下，为任意 KeyValueStoreInterface<K,V> 增加命中统计。
 * 语义（本轮非并发版本）：
 *  - 仅当 get 成功命中（key 存在）时计数 +1：
 *      * getOrNull(key): map.get(key) 非 null -> +1
 *      * getOrDefault(key, def): 只有 key 存在才 +1；缺席返回 def 不计数
 *      * getOrThrow(key): 命中则 +1；缺席抛 NoSuchElementException
 *  - remove(key): 移除该 key，并清除其命中计数
 *  - clear(): 清空存储，并将所有命中计数及 totalHits 清零
 *  - topHits(k): 命中数降序；若相同，按 key 的“自然顺序”；若 key 不可比较则按 toString()
 */
public class HitCountingStore<K, V>
        implements KeyValueStoreInterface<K, V>, HitCountReadable<K> {

    private final KeyValueStoreInterface<K, V> delegate;
    private final Map<K, Long> hitCounts = new HashMap<>();
    private long totalHits = 0L;

    /** 命中数相同的情况下，用于比较 key 的比较器 */
    private final Comparator<K> keyComparator;

    public HitCountingStore(KeyValueStoreInterface<K, V> delegate) {
        this(delegate, null);
    }

    public HitCountingStore(KeyValueStoreInterface<K, V> delegate, Comparator<K> keyComparator) {
        if (delegate == null) throw new IllegalArgumentException("delegate must not be null");
        this.delegate = delegate;
        this.keyComparator = (keyComparator != null) ? keyComparator : naturalOrToStringComparator();
    }

    @SuppressWarnings({"unchecked","rawtypes"})
    private Comparator<K> naturalOrToStringComparator() {
        return (a, b) -> {
            if (a == b) return 0;
            if (a == null) return -1; // Round1 不允许 null key，这里仅兜底
            if (b == null) return 1;
            if (a instanceof Comparable && a.getClass().isInstance(b)) {
                int c = ((Comparable) a).compareTo(b);
                if (c != 0) return c;
                return a.toString().compareTo(b.toString());
            }
            return a.toString().compareTo(b.toString());
        };
    }

    private void inc(K key) {
        hitCounts.merge(key, 1L, Long::sum);
        if (totalHits != Long.MAX_VALUE) { // 简单溢出保护（到达 LONG_MAX 后不再增加）
            totalHits++;
        }
    }

    /* ---------------- KeyValueStoreInterface 代理并植入计数逻辑 ---------------- */

    @Override
    public void put(K key, V value) {
        delegate.put(key, value);
        // put 不影响计数
    }

    @Override
    public V getOrNull(K key) {
        V v = delegate.getOrNull(key);
        if (v != null) inc(key);
        return v;
    }

    @Override
    public V getOrDefault(K key, V defaultValue) {
        // 只在 key 存在时计数；否则返回 defaultValue 且不计数
        V v = delegate.getOrNull(key);
        if (v != null) {
            inc(key);
            return v;
        }
        return defaultValue;
    }

    @Override
    public V getOrThrow(K key) throws NoSuchElementException {
        // 复用 Round1 语义：缺席抛异常；命中则计数
        V v = delegate.getOrNull(key);
        if (v == null) throw new NoSuchElementException("Key not found: " + key);
        inc(key);
        return v;
    }

    @Override
    public V remove(K key) {
        V old = delegate.remove(key);
        // 设计选择：移除即重置该 key 的命中数
        hitCounts.remove(key);
        return old;
    }

    @Override
    public boolean containsKey(K key) {
        return delegate.containsKey(key);
    }

    @Override
    public int size() {
        return delegate.size();
    }

    @Override
    public void clear() {
        delegate.clear();
        hitCounts.clear();
        totalHits = 0L; // 设计选择：clear 后计数也清零
    }

    /* ---------------- HitCountReadable ---------------- */

    @Override
    public long getHitCount(K key) {
        if (key == null) throw new IllegalArgumentException("key must not be null");
        return hitCounts.getOrDefault(key, 0L);
    }

    @Override
    public long getTotalHits() {
        return totalHits;
    }

    @Override
    public Map<K, Long> topHits(int k) {
        if (k < 0) throw new IllegalArgumentException("k must be >= 0");
        int limit = Math.min(k, hitCounts.size());

        return hitCounts.entrySet()
                .stream()
                .sorted((e1, e2) -> {
                    int byCountDesc = Long.compare(e2.getValue(), e1.getValue());
                    if (byCountDesc != 0) return byCountDesc;
                    return keyComparator.compare(e1.getKey(), e2.getKey());
                })
                .limit(limit)
                .collect(
                        LinkedHashMap::new,
                        (m, e) -> m.put(e.getKey(), e.getValue()),
                        Map::putAll
                );
    }
}
