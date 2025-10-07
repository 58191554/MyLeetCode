from collections import deque
from typing import List, Optional

class Solution:
    def findBottlenecks(self, n: int, edges: List[List[int]]) -> List[int]:
        g = {}
        deg = [0] * n
        for u, v in edges:
            g.setdefault(u, [])
            g[u].append(v)
            deg[v] += 1
        q = deque()
        for i in range(n):
            if deg[i] == 0:
                q.append(i)
        result = []
        while q:
            size = len(q)
            if size == 1:
                result.append(q[0])
            for _ in range(size):
                x = q.popleft()
                if x not in g:
                    continue
                for y in g[x]:
                    deg[y] -= 1
                    if deg[y] == 0:
                        q.append(y)
        return result
