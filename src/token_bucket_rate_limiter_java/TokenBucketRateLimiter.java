package token_bucket_rate_limiter_java;

import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.locks.Condition;

public class TokenBucketRateLimiter {
    private final double ratePerSecond;
    private final int capacity;

    private final ReentrantLock lock = new ReentrantLock();
    private final Condition changed = lock.newCondition();

    private double stored;
    private long lastRefillNanos;

    public TokenBucketRateLimiter(double ratePerSecond, int capacity) {
        this.ratePerSecond = ratePerSecond;
        this.capacity = capacity;
        this.stored = capacity;
        this.lastRefillNanos = System.nanoTime();
    }

    // no blocking
    public boolean tryAcquire(int permits) {
        lock.lock();
        try {
            long nowNano = System.nanoTime();
            double avaibleCount = ratePerSecond * (nowNano - lastRefillNanos) / 1_000_000_000.0;
            stored = Math.min(stored + avaibleCount, capacity);
            lastRefillNanos = nowNano;
            if (stored >= permits) {
                stored -= permits;
                changed.signal();
                return true;
            } else {
                return false;
            }
        } finally {
            lock.unlock();
        }
    }

    // blocking
    public void acquire(int permits) {
        lock.lock();
        try {
            while (true) {
                long waitNano = 
            }
        }
    }
}
