package find_optimal_commute_java;

import java.util.*;

public class BestTransportSelector {
    private static final int[][] dirs = {
        {0, 1}, {0, -1}, {1, 0}, {-1, 0}
    };
    public static int bestTransport(String[][] grid, int[] cost, int[] time) {
        int start_i = -1, start_j = -1;
        int m = grid.length, n = grid[0].length;
        for (int i = 0; i < m; i++) {
            if (start_i != -1) break;
            for (int j = 0; j < n; j++) {
                if (grid[i][j].equals("S")) {
                    start_i = i;
                    start_j = j;
                    break;
                }
            }
        }
        int[][] visited = new int[m][n];
        Queue<int[]> queue = new LinkedList<>();
        int[] disK = new int[cost.length];
        Arrays.fill(disK, -1);
        for (int i = 1; i <= cost.length; i++) {
            queue.add(new int[]{start_i, start_j, 0, i});
        }
        while (!queue.isEmpty()) {
            int[] es = queue.poll();
            int i = es[0], j = es[1], d = es[2], k = es[3];
            // System.out.println("i = " + i + ", j = " + j + ", d = " + d + ", k = " + k);
            if (visited[i][j] == 1) {
                continue;
            }
            if (!grid[i][j].equals("S")){
                visited[i][j] = 1;
            }
            if (!grid[i][j].equals("D")) {
                for (int[] dir: dirs) {
                    int ii = i + dir[0], jj = j + dir[1];
                    if (0 <= ii && ii < m && 0 <= jj && jj < n) {
                        if (grid[ii][jj].equals(String.valueOf(k))){
                            queue.add(new int[]{ii, jj, d + 1, k});
                        } else if (grid[ii][jj].equals("D")) {
                            disK[k - 1] = d + 1;
                        }
                    }
                }
            }
        }
        // System.out.println(Arrays.toString(disK));
        int resultTime = Integer.MAX_VALUE, resultCost = Integer.MAX_VALUE, bestTransport = -1;
        for (int k = 0; k < cost.length; k++) {
            if (disK[k] != -1 && disK[k] * time[k] < resultTime) {
                resultTime = Math.min(resultTime, disK[k] * time[k]);
                resultCost = disK[k] * cost[k];
                bestTransport = k + 1;
            } else if (disK[k] != -1 && disK[k] * time[k] == resultTime && disK[k] * cost[k] < resultCost) {
                resultCost = disK[k] * cost[k];
                bestTransport = k + 1;
            }
        }
        return bestTransport;
    }

    public static void main(String[] args) {
        // 小工具：跑用例并显示期望值
        Runnable all = () -> {};
        class T {
            void runTest(int id, String[][] grid, int[] cost, int[] time, int expected) {
                int ans = bestTransport(grid, cost, time);
                System.out.printf("TC%-2d -> ans=%d, expected=%d %s%n",
                        id, ans, expected, (ans == expected ? "✅" : "❌"));
            }
        }
        T t = new T();
    
        // -------------------------
        // TC1 基本示例（题干中的样例）
        // 仅工具1可达
        // 期望：1
        // -------------------------
        String[][] g1 = {
            {"S","1","1","2"},
            {"2","1","2","2"},
            {"2","1","1","D"},
            {"3","3","1","2"}
        };
        int[] cost1 = {3, 1, 5};
        int[] time1 = {1, 2, 1};
        t.runTest(1, g1, cost1, time1, 1);
    
        // -------------------------
        // TC2 time 相同，用 cost 决胜
        // 两条等长通道（1/2 都能走，步数相同），time 一样，cost(2) 更低
        // 期望：2
        // -------------------------
        String[][] g2 = {
            {"S","1","1","1"},
            {"2","2","2","D"}
        };
        int[] cost2 = {5, 3}; // 工具1=5, 工具2=3
        int[] time2 = {2, 2}; // time 相同
        t.runTest(2, g2, cost2, time2, 2);
    
        // -------------------------
        // TC3 优先最短总 time，即便 cost 更高
        // 同 g2，但设 time1 更小 -> 选 1
        // 期望：1
        // -------------------------
        int[] cost3 = {100, 1};
        int[] time3 = {1, 3}; // tool1 总 time 更小
        t.runTest(3, g2, cost3, time3, 1);
    
        // -------------------------
        // TC4 全部不可达 -> -1
        // 网格里只有“4”，但工具只有 1..3
        // 期望：-1
        // -------------------------
        String[][] g4 = {
            {"S","4","4"},
            {"4","4","4"},
            {"4","4","D"}
        };
        int[] cost4 = {1,1,1};
        int[] time4 = {1,1,1};
        t.runTest(4, g4, cost4, time4, -1);
    
        // -------------------------
        // TC5 time、cost 都相同 -> 选编号更小的
        // 期望：1
        // -------------------------
        int[] cost5 = {5,5};
        int[] time5 = {2,2};
        t.runTest(5, g2, cost5, time5, 1);
    
        // -------------------------
        // TC6 支持多位编号（工具 10）
        // 只有“10”通道能到 D
        // 期望：10
        // -------------------------
        String[][] g6 = {
            {"S","10","10","D"}
        };
        int[] cost6 = {9,9,9,9,9,9,9,9,9,2}; // 长度=10（工具1..10）
        int[] time6 = {9,9,9,9,9,9,9,9,9,1};
        t.runTest(6, g6, cost6, time6, 10);
    
        // -------------------------
        // TC7 S 与 D 相邻
        // 步数=1，对所有可用工具都成立；比较 time 优先
        // 期望：2（因为 time2 更小）
        // -------------------------
        String[][] g7 = {
            {"S","D"}
        };
        int[] cost7 = {7, 100};
        int[] time7 = {5, 1};
        t.runTest(7, g7, cost7, time7, 2);
    
        // -------------------------
        // TC8 只有工具3有可达路径（较长），其余均不可达
        // 期望：3
        // -------------------------
        String[][] g8 = {
            {"S","3","9","3","3","D"},
            {"9","3","9","9","3","9"},
            {"9","3","3","3","3","9"}
        };
        int[] cost8 = {9,9,2};   // 随便给
        int[] time8 = {9,9,1};   // 只有 3 可达
        t.runTest(8, g8, cost8, time8, 3);
    
        // -------------------------
        // TC9 步数不同但单步 time 不同 -> 以总 time 决胜
        // 工具1路径短(4步)但每步更慢；工具2路径长(6步)但更快
        // 4*3=12 vs 6*1=6 -> 选 2
        // 期望：2
        // -------------------------
        String[][] g9 = {
            {"S","1","1","1","D"},
            {"2","2","2","2","2"}
        };
        int[] cost9 = {10, 10};
        int[] time9 = {3, 1};
        t.runTest(9, g9, cost9, time9, 2);
    
        // -------------------------
        // TC10 多工具都可达，time 相同，用 cost 决胜，再相同选编号小
        // 这里设3个工具：1/2/3 都可达，time 相同，cost1=cost2<cost3 -> 选编号小：1
        // 期望：1
        // -------------------------
        String[][] g10 = {
            {"S","1","1","D"},
            {"2","2","2","D"},
            {"3","3","3","D"}
        };
        int[] cost10 = {5,5,6};
        int[] time10 = {2,2,2};
        t.runTest(10, g10, cost10, time10, 1);
    }
}
