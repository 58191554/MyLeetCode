package find_optimal_commute_java;

import java.util.*;

public class BestTransportSelectorRef {

    static class Point {
        int r, c, d;
        Point(int r, int c, int d) { this.r = r; this.c = c; this.d = d; }
    }

    public static int bestTransport(String[][] grid, int[] cost, int[] time) {
        int R = grid.length, C = grid[0].length;
        int N = cost.length; // 工具编号 1..N

        int sr = -1, sc = -1, dr = -1, dc = -1;
        for (int i = 0; i < R; i++) {
            for (int j = 0; j < C; j++) {
                if (grid[i][j].equals("S")) { sr = i; sc = j; }
                else if (grid[i][j].equals("D")) { dr = i; dc = j; }
            }
        }
        if (sr == -1 || dr == -1) return -1; // 无 S 或 D

        // 保存当前最优：(time, cost, id)
        long bestTime = Long.MAX_VALUE;
        long bestCost = Long.MAX_VALUE;
        int bestId = -1;

        for (int k = 1; k <= N; k++) {
            int steps = bfsForTool(grid, sr, sc, dr, dc, k);
            if (steps < 0) continue; // 不可达

            long totalTime = (long) steps * time[k - 1];
            long totalCost = (long) steps * cost[k - 1];

            if (totalTime < bestTime ||
               (totalTime == bestTime && totalCost < bestCost) ||
               (totalTime == bestTime && totalCost == bestCost && k < bestId)) {
                bestTime = totalTime;
                bestCost = totalCost;
                bestId = k;
            }
        }
        return bestId;
    }

    // 仅能走 "S"、"D"、以及等于工具编号的格子
    private static int bfsForTool(String[][] grid, int sr, int sc, int dr, int dc, int toolId) {
        int R = grid.length, C = grid[0].length;
        boolean[][] vis = new boolean[R][C];
        Deque<Point> q = new ArrayDeque<>();
        q.offer(new Point(sr, sc, 0));
        vis[sr][sc] = true;

        String allow = String.valueOf(toolId);
        int[] dR = {1, -1, 0, 0};
        int[] dC = {0, 0, 1, -1};

        while (!q.isEmpty()) {
            Point cur = q.poll();
            if (cur.r == dr && cur.c == dc) return cur.d;

            for (int t = 0; t < 4; t++) {
                int nr = cur.r + dR[t], nc = cur.c + dC[t];
                if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;
                if (vis[nr][nc]) continue;

                String cell = grid[nr][nc];
                if (cell.equals("S") || cell.equals("D") || cell.equals(allow)) {
                    vis[nr][nc] = true;
                    q.offer(new Point(nr, nc, cur.d + 1));
                }
            }
        }
        return -1; // 不可达
    }

    // 简单跑一下示例
    public static void main(String[] args) {
        String[][] grid = {
            {"S","1","1","2"},
            {"2","1","2","2"},
            {"2","1","1","D"},
            {"3","3","1","2"}
        };
        int[] cost = {3, 1, 5}; // 工具 1,2,3
        int[] time = {1, 2, 1};

        int ans = bestTransport(grid, cost, time);
        System.out.println(ans); // 期望输出：1
    }
}
