import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

public class BoundedBlockingQueue<E> {
    private final E[] items;
    private final int capacity;
    private int head = 0, tail = 0, count = 0;

    private final ReentrantLock lock = new ReentrantLock();
    private final Condition notFull  = lock.newCondition();
    private final Condition notEmpty = lock.newCondition();

    @SuppressWarnings("unchecked")
    public BoundedBlockingQueue(int capacity) {
        if (capacity <= 0) throw new IllegalArgumentException("capacity must be > 0");
        this.capacity = capacity;
        this.items = (E[]) new Object[capacity];
    }

    public void put(E e) throws InterruptedException {
        lock.lock();
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
        lock.lock();
        E result = null;
        try {
            while (count == 0) {
                notEmpty.await();
            }
            result = items[head];
            head = (head + 1) % capacity;
            count--;
            notFull.signal();
        } finally {
            lock.unlock();
        }
        return result;
    }

    public int size() {
        lock.lock();
        try {
            return count;
        } finally {
            lock.unlock();
        }
    }
}
