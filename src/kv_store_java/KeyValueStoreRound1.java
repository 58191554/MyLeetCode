package kv_store_java;

import java.util.Map;
import java.util.NoSuchElementException;
import java.util.HashMap;

public class KeyValueStoreRound1<K, V> implements KeyValueStoreInterface<K, V> {
    private final Map<K, V> map;
    public KeyValueStoreRound1() {
        this.map = new HashMap<>();
    }

    private static <T> void requireNonNullArg(T x, String name) {
        if (x == null) throw new IllegalArgumentException(name + "must not be null");
    }

    @Override
    public void put(K key, V value) {
        requireNonNullArg(key, "key");
        requireNonNullArg(value, "value");
        map.put(key, value);
    }

    @Override
    public V getOrNull(K key) {
        requireNonNullArg(key, "key");
        return map.get(key);
    }

    @Override
    public V getOrDefault(K key, V defaultValue) {
        requireNonNullArg(key, "key");
        // allow defaultValue to be null? Here we also disallow to avoid ambiguity.
        requireNonNullArg(defaultValue, "defaultValue");
        return map.getOrDefault(key, defaultValue);
    }

    @Override
    public V getOrThrow(K key) throws NoSuchElementException {
        requireNonNullArg(key, "key");
        V v = map.get(key);
        if (v == null) {
            throw new NoSuchElementException("Key not found: " + key);
        }
        return v;
    }

    @Override
    public V remove(K key) {
        requireNonNullArg(key, "key");
        return map.remove(key);
    }

    @Override
    public boolean containsKey(K key) {
        requireNonNullArg(key, "key");
        return map.containsKey(key);
    }

    @Override
    public int size() {
        return map.size();
    }

    @Override
    public void clear() {
        map.clear();
    }
}
