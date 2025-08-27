import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

public class BoundedBlockingQueueCorrected<E> {
    private final E[] items;
    private final int capacity;
    private int head = 0, tail = 0, count = 0;

    private final ReentrantLock lock = new ReentrantLock();
    private final Condition notFull  = lock.newCondition();
    private final Condition notEmpty = lock.newCondition();

    @SuppressWarnings("unchecked")
    public BoundedBlockingQueueCorrected(int capacity) {
        if (capacity <= 0) throw new IllegalArgumentException("capacity must be > 0");
        this.capacity = capacity;
        this.items = (E[]) new Object[capacity];
    }

    public void put(E e) throws InterruptedException {
        lock.lockInterruptibly(); // Use lockInterruptibly for proper interrupt handling
        try {
            while (count == capacity) {
                notFull.await();
            }
            items[tail] = e;
            tail = (tail + 1) % capacity;
            count++;
            notEmpty.signal();
        } finally {
            lock.unlock();
        }
    }

    public E take() throws InterruptedException {
        lock.lockInterruptibly(); // Use lockInterruptibly for proper interrupt handling
        try {
            while (count == 0) {
                notEmpty.await();
            }
            E result = items[head];
            items[head] = null; // Help GC
            head = (head + 1) % capacity;
            count--;
            notFull.signal();
            return result;
        } finally {
            lock.unlock();
        }
    }

    public int size() {
        lock.lock(); // size() doesn't need to be interruptible
        try {
            return count;
        } finally {
            lock.unlock();
        }
    }
    
    public int remainingCapacity() {
        lock.lock();
        try {
            return capacity - count;
        } finally {
            lock.unlock();
        }
    }
}
