题目：实现一个线程安全的 TokenBucketRateLimiter
目标

实现一个可在多线程下使用的令牌桶限流器，支持立即尝试、阻塞等待、超时三种获取令牌的方式。不得 busy-wait；需要正确处理中断与时间计算。

需求 & API

类名：TokenBucketRateLimiter

构造：

TokenBucketRateLimiter(double permitsPerSecond, int burstCapacity)

permitsPerSecond > 0：平均每秒产生的令牌数（速率）。

burstCapacity >= 1：桶的最大容量（瞬时突发上限）。

方法：

boolean tryAcquire()
立刻尝试获取 1 个令牌；成功返回 true，失败返回 false（不阻塞）。

boolean tryAcquire(int permits)
立刻尝试获取 permits 个令牌；成功返回 true，失败返回 false。

void acquire(int permits) throws InterruptedException
阻塞直到拿到 permits 个令牌或被中断。被中断时立刻抛出 InterruptedException。

boolean acquire(int permits, long timeout, TimeUnit unit) throws InterruptedException
在超时时间内等待拿到 permits；成功返回 true，超时返回 false；中断立刻抛出。

int getCapacity() / double getRate() / int getStoredPermits()（可选，读到的值需具备可见性一致性）

语义约束

线程安全：多线程同时调用任意方法，状态不乱。

不 busy-wait：用 Condition.awaitNanos(...) 等阻塞等待，不能 sleep 轮询。

时间正确：使用 System.nanoTime() 做时间差（单调时钟），不要用 currentTimeMillis()。

中断语义：阻塞等待时被中断，立刻抛出 InterruptedException 并不吞掉中断位。

边界：permits <= burstCapacity 时才可能成功；否则立即失败（或抛 IllegalArgumentException，你选一种并保持一致）。

精度：内部可用 double 存储令牌；每次先按经过时间懒惰补发令牌，再尝试扣减；令牌数不得超过 burstCapacity。