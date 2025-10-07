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

from typing import List, Optional
from math import inf
from collections import deque
class Solution:
    def findOptimalCommute(self, grid: List[List[str]], modes: List[str], costs: List[int], times: List[int]) -> str:
        startX, startY = None, None
        m, n = len(grid), len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == "S":
                    startX, startY = i, j
                    break
            if startX != None and startY != None:
                break
        k = len(modes)
        q = deque([(startX, startY, i, 0) for i in range(1, k + 1)])
        visited = [[0] * n for _ in range(m)]
        startMode = [0] * (k + 1)
        dis = [inf] * (k + 1)
        while q:
            x, y, mode, d = q.popleft()
            if grid[x][y] == "S":
                if startMode[mode]:
                    continue
                startMode[mode] = 1             
            else:
                if visited[x][y]:
                    continue
                visited[x][y] = 1
            
            for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                xx, yy = x + dx, y + dy
                if 0 <= xx < m and 0 <= yy < n:
                    if grid[xx][yy] == str(mode):
                        q.append([xx, yy, mode, d + 1])
                    elif grid[xx][yy] == "D":
                        print(xx, yy, mode, d)
                        if dis[mode] == inf:
                            dis[mode] = d   
        minCost = inf; minTime = inf; result = ""
        print(dis)
        for i, mode in enumerate(modes):
            if minTime == dis[i + 1] * times[i] and minCost > dis[i + 1] * costs[i]:
                minCost = dis[i + 1] * costs[i]
                result = mode
            elif minTime > dis[i + 1] * times[i]:
                minTime = dis[i + 1] * times[i]
                minCost = dis[i + 1] * costs[i]
                result = mode
        return result
                