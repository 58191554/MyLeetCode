package kv_store_java;

import java.util.Map;

public interface HitCountReadable<K> {
    /** 返回 key 的累计命中次数（不存在则为 0） */
    long getHitCount(K key);

    /** 返回全局命中次数（所有成功 get 的总和） */
    long getTotalHits();

    /**
     * 按命中数降序返回 Top-k；命中数相同，用 key 排序（见实现中的比较器说明）。
     * 返回的 Map 保持有序（LinkedHashMap）。
     */
    Map<K, Long> topHits(int k);
}
