import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.ArrayList;
import java.util.List;

public class SimpleBoundedBlockingQueueTest {
    
    public static void main(String[] args) {
        System.out.println("Running BoundedBlockingQueue tests...");
        
        try {
            testBasicOperations();
            testCapacityValidation();
            testCircularBuffer();
            testBlockingBehavior();
            testConcurrency();
            testInterruption();
            testNullElements();
            
            System.out.println("\n🎉 All tests passed!");
        } catch (Exception e) {
            System.err.println("❌ Test failed: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private static void testBasicOperations() throws InterruptedException {
        System.out.println("✓ Testing basic put/take operations...");
        BoundedBlockingQueue<Integer> queue = new BoundedBlockingQueue<>(3);
        
        // Test put and take
        queue.put(1);
        queue.put(2);
        assertEqual(2, queue.size(), "Size should be 2");
        
        Integer item1 = queue.take();
        Integer item2 = queue.take();
        assertEqual(Integer.valueOf(1), item1, "First item should be 1");
        assertEqual(Integer.valueOf(2), item2, "Second item should be 2");
        assertEqual(0, queue.size(), "Size should be 0");
    }
    
    private static void testCapacityValidation() {
        System.out.println("✓ Testing capacity validation...");
        try {
            new BoundedBlockingQueue<>(0);
            throw new AssertionError("Should have thrown IllegalArgumentException");
        } catch (IllegalArgumentException e) {
            // Expected
        }
        
        try {
            new BoundedBlockingQueue<>(-1);
            throw new AssertionError("Should have thrown IllegalArgumentException");
        } catch (IllegalArgumentException e) {
            // Expected
        }
    }
    
    private static void testCircularBuffer() throws InterruptedException {
        System.out.println("✓ Testing circular buffer behavior...");
        BoundedBlockingQueue<Integer> queue = new BoundedBlockingQueue<>(3);
        
        // Fill queue
        queue.put(1);
        queue.put(2);
        queue.put(3);
        
        // Test circular behavior
        assertEqual(Integer.valueOf(1), queue.take(), "First item should be 1");
        queue.put(4);
        assertEqual(Integer.valueOf(2), queue.take(), "Second item should be 2");
        assertEqual(Integer.valueOf(3), queue.take(), "Third item should be 3");
        assertEqual(Integer.valueOf(4), queue.take(), "Fourth item should be 4");
    }
    
    private static void testBlockingBehavior() throws InterruptedException {
        System.out.println("✓ Testing blocking behavior...");
        BoundedBlockingQueue<Integer> queue = new BoundedBlockingQueue<>(2);
        
        // Fill queue
        queue.put(1);
        queue.put(2);
        
        // Test put blocks when full
        CountDownLatch latch = new CountDownLatch(1);
        AtomicInteger putResult = new AtomicInteger(-1);
        
        Thread producer = new Thread(() -> {
            try {
                latch.countDown();
                queue.put(3); // Should block
                putResult.set(3);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        producer.start();
        latch.await();
        Thread.sleep(100); // Let producer block
        
        assertEqual(2, queue.size(), "Queue should still be full");
        assertEqual(-1, putResult.get(), "Put should still be blocked");
        
        // Unblock by taking an item
        queue.take();
        producer.join(1000);
        assertEqual(3, putResult.get(), "Put should have completed");
        
        // Test take blocks when empty
        queue.take(); // Empty the queue
        queue.take();
        
        CountDownLatch takeLatch = new CountDownLatch(1);
        AtomicInteger takeResult = new AtomicInteger(-1);
        
        Thread consumer = new Thread(() -> {
            try {
                takeLatch.countDown();
                Integer result = queue.take(); // Should block
                takeResult.set(result);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        consumer.start();
        takeLatch.await();
        Thread.sleep(100); // Let consumer block
        
        assertEqual(0, queue.size(), "Queue should still be empty");
        assertEqual(-1, takeResult.get(), "Take should still be blocked");
        
        // Unblock by putting an item
        queue.put(42);
        consumer.join(1000);
        assertEqual(42, takeResult.get(), "Take should have completed");
    }
    
    private static void testConcurrency() throws InterruptedException {
        System.out.println("✓ Testing producer-consumer concurrency...");
        BoundedBlockingQueue<Integer> queue = new BoundedBlockingQueue<>(5);
        
        final int itemCount = 100;
        List<Integer> consumed = new ArrayList<>();
        Object lock = new Object();
        
        // Producer
        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < itemCount; i++) {
                    queue.put(i);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Consumer
        Thread consumer = new Thread(() -> {
            try {
                for (int i = 0; i < itemCount; i++) {
                    Integer item = queue.take();
                    synchronized (lock) {
                        consumed.add(item);
                    }
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        producer.start();
        consumer.start();
        
        producer.join(5000);
        consumer.join(5000);
        
        assertEqual(itemCount, consumed.size(), "Should consume all items");
        assertEqual(0, queue.size(), "Queue should be empty");
        
        // Verify order (should be 0, 1, 2, ..., 99)
        for (int i = 0; i < itemCount; i++) {
            assertEqual(Integer.valueOf(i), consumed.get(i), "Item " + i + " should match");
        }
    }
    
    private static void testInterruption() throws InterruptedException {
        System.out.println("✓ Testing interruption handling...");
        BoundedBlockingQueue<Integer> queue = new BoundedBlockingQueue<>(1);
        
        // Note: Your current implementation uses lock.lock() instead of lock.lockInterruptibly()
        // So this test will demonstrate the difference
        
        queue.put(1); // Fill queue
        
        AtomicInteger exceptionCount = new AtomicInteger(0);
        
        Thread producer = new Thread(() -> {
            try {
                Thread.sleep(100); // Let main thread interrupt us
                queue.put(2); // This will block
            } catch (InterruptedException e) {
                exceptionCount.incrementAndGet();
                Thread.currentThread().interrupt();
            }
        });
        
        producer.start();
        Thread.sleep(50);
        producer.interrupt();
        producer.join(1000);
        
        System.out.println("  Note: Current implementation may not handle interruption properly");
        System.out.println("  Consider using lock.lockInterruptibly() instead of lock.lock()");
    }
    
    private static void testNullElements() throws InterruptedException {
        System.out.println("✓ Testing null elements...");
        BoundedBlockingQueue<String> queue = new BoundedBlockingQueue<>(2);
        
        queue.put(null);
        queue.put("test");
        
        String item1 = queue.take();
        String item2 = queue.take();
        
        assertEqual(null, item1, "First item should be null");
        assertEqual("test", item2, "Second item should be 'test'");
    }
    
    // Helper assertion methods
    private static void assertEqual(Object expected, Object actual, String message) {
        if (!java.util.Objects.equals(expected, actual)) {
            throw new AssertionError(message + " - Expected: " + expected + ", Actual: " + actual);
        }
    }
    
    private static void assertEqual(int expected, int actual, String message) {
        if (expected != actual) {
            throw new AssertionError(message + " - Expected: " + expected + ", Actual: " + actual);
        }
    }
}
