from typing import List, Tuple
from math import inf
import heapq

class Solution:
    def findOptimalCommute(
        self,
        grid: List[List[str]],
        modes: List[str],
        costs: List[int],
        times: List[int],
        swtchCost: int,
        switchTime: int
    ) -> Tuple[int, int]:
        m, n = len(grid), len(grid[0])
        sx = sy = dx = dy = -1
        for i in range(m):
            for j in range(n):
                if grid[i][j] == "S":
                    sx, sy = i, j
                elif grid[i][j] == "D":
                    dx, dy = i, j

        # Dijkstra: 状态=(time, cost, x, y, mode)，mode: 0=无模式（仅 S/D）
        pq = [(0, 0, sx, sy, 0)]
        dist = {}  # (x,y,mode) -> (time, cost)
        dist[(sx, sy, 0)] = (0, 0)

        DIRS = [(0,1),(0,-1),(1,0),(-1,0)]

        while pq:
            d, c, i, j, mode = heapq.heappop(pq)
            if dist.get((i, j, mode), (inf, inf)) != (d, c):
                continue

            # 抵达 D（用 mode=0 表示在 D）
            if i == dx and j == dy and mode == 0:
                return d, c

            for dx4, dy4 in DIRS:
                ii, jj = i + dx4, j + dy4
                if not (0 <= ii < m and 0 <= jj < n):
                    continue
                ch = grid[ii][jj]
                if ch == "X" or ch == "S":
                    continue

                if ch == "D":
                    nd, nc = d, c  # 进入 D 零代价
                    key = (ii, jj, 0)
                    if (nd, nc) < dist.get(key, (inf, inf)):
                        dist[key] = (nd, nc)
                        heapq.heappush(pq, (nd, nc, ii, jj, 0))
                    continue

                if ch.isdigit():
                    nx_mode = int(ch)
                    step_t = times[nx_mode - 1]
                    step_c = costs[nx_mode - 1]
                    if mode != 0 and nx_mode != mode:
                        step_t += switchTime
                        step_c += swtchCost
                    nd, nc = d + step_t, c + step_c
                    key = (ii, jj, nx_mode)
                    if (nd, nc) < dist.get(key, (inf, inf)):
                        dist[key] = (nd, nc)
                        heapq.heappush(pq, (nd, nc, ii, jj, nx_mode))

        return inf, inf  # 不可达
