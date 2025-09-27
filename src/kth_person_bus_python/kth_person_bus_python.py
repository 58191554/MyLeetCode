from typing import List, Tuple

class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0]*(n+1)

    def add(self, i: int, delta: int):
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def sum(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def kth(self, k: int) -> int:
        """Smallest idx with prefix sum >= k. Assumes 1 <= k <= sum(n)."""
        idx = 0
        bit_mask = 1 << (self.n.bit_length())  # highest power of two >= n
        while bit_mask:
            nxt = idx + bit_mask
            if nxt <= self.n and self.bit[nxt] < k:
                k -= self.bit[nxt]
                idx = nxt
            bit_mask >>= 1
        return idx + 1

def kthPerson(k: int, p: List[int], q: List[int]) -> List[int]:
    n = len(p)
    # People as (patience, index). Indices are 1-based for Fenwick convenience.
    people: List[Tuple[int, int]] = sorted((p[i], i+1) for i in range(n))  # asc by patience
    # Queries as (time, original_index), sorted desc by time.
    qs: List[Tuple[int, int]] = sorted(((q[i], i) for i in range(len(q))), reverse=True)

    bit = Fenwick(n)
    ans = [0]*len(q)

    ptr = n - 1  # walk people from the end (largest patience)
    for t, qi in qs:
        # Add everyone with p >= t
        while ptr >= 0 and people[ptr][0] >= t:
            _, idx = people[ptr]
            bit.add(idx, 1)
            ptr -= 1
        total = bit.sum(n)
        if total >= k:
            ans[qi] = bit.kth(k)
        else:
            ans[qi] = 0
    return ans

# Example
if __name__ == "__main__":
    k = 2
    p = [1, 2, 3, 4]
    q = [1, 3, 4]
    print(kthPerson(k, p, q))  # [2, 4, 0]
