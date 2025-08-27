"""
# Find Optimal Commute
You are given a city map as an `R × C` integer matrix `grid`. Each cell value is in 
`{1, 2, …, K}` and represents a transportation mode (e.g., `1=walk`, `2=bike`, `3=bus`, 
`4=car`, …).
You are also given two arrays of length `K`:
* `time[m]` — the time cost for entering a cell whose mode is `m` (1-indexed),
* `cost[m]` — the monetary cost for entering a cell whose mode is `m` (1-indexed).

You start at cell `start = (sr, sc)` and want to reach `end = (tr, tc)`. From any cell, 
you may move to one of its four neighbors (up, down, left, right) if it stays within the 
grid.
When you **enter** a neighbor cell `(nr, nc)`, your totals increase by:

* `total_time += time[ grid[nr][nc] ]`
* `total_cost += cost[ grid[nr][nc] ]`

> The starting cell does **not** add time or cost (only entering new cells does).

## Objective

Among all valid paths from `start` to `end`:

1. Minimize total time.
2. If multiple paths have the same total time, break ties by minimizing total cost.

## Output

Return a pair `(min_total_time, min_total_cost)` for an optimal path.
If `end` is unreachable, return `(-1, -1)` (or any sentinel agreed upon).

## Constraints (typical)

* `1 ≤ R, C ≤ 10^3`
* `1 ≤ K ≤ 10`
* `time[m] > 0`, `cost[m] ≥ 0`
* `start` and `end` are valid indices within the grid

## Example

```
grid =
1 2 1
1 3 2
1 1 1

time = [ -, 1, 2, 4 ]   // 1-indexed: mode 1→1 min, 2→2 min, 3→4 min
cost = [ -, 3, 1, 5 ]   // mode 1→$3, 2→$1, 3→$5

start = (0, 0), end = (2, 2)
```

Find a path from `(0,0)` to `(2,2)` with minimum total time; if tied, choose the one 
with lower total cost.

> Implementation hint (not required by the statement): Model the grid as a graph and 
run Dijkstra with a **lexicographic** distance `(time, cost)` so that time is primary 
and cost is the tiebreaker.
"""

from typing import List
import heapq
import math
class Solution:
    def find_optimal_commute(grid: List[List[int]], time: List[int], cost: List[int], start: tuple, end: tuple) -> tuple:
        pq = []
        heapq.heapify(pq)
        heapq.heappush(pq, [0, 0, start[0], start[1]])
        m, n = len(grid), len(grid[0])
        dis = [[math.inf] * n for _ in range(m)]
        spend = [[math.inf] * n for _ in range(m)]
        while pq:
            d, c, i, j = heapq.heappop(pq)
            c = -c
            if d > dis[i][j]:
                continue
            if d < dis[i][j]:
                dis[i][j] = d
                spend[i][j] = c
            elif d == dis[i][j] and c < spend[i][j]:
                spend[i][j] = c
            else:
                continue
            for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                ii, jj = i + dx, j + dy
                if 0 <= ii < m and 0 <= jj < n:
                    method = grid[ii][jj]
                    heapq.heappush(pq, [d + time[method], -c - cost[method], ii, jj])
        return dis[end[0]][end[1]], spend[end[0]][end[1]]
        
        