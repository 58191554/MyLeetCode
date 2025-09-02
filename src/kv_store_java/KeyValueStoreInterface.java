package kv_store_java;

import java.util.NoSuchElementException;

public interface KeyValueStoreInterface<K, V> {
    void put(K key, V value);
    V getOrNull(K key);
    V getOrDefault(K key, V defautValue);
    V getOrThrow(K key) throws NoSuchElementException;
    V remove(K key);
    boolean containsKey(K key);
    int size();
    void clear();
}
