Find Optimal Commute
Medium
Greedy
Breadth First Search
Interview Stages
Screening
Onsite
Frequency
Asked By

Last Reported
2 months ago
You are commuting across a simplified map of San Francisco, represented as a 2D grid. Each cell on the grid is one of the following:

'S': Your home location (starting point).
'D': Your office location (destination).
A digit from '1' to k: A street segment reserved for exactly one transportation mode.
'X': An impassable roadblock.
You are also given three arrays with length k:

modes: The name of each available transportation mode.
times: The time (in minutes) required to traverse a single block using each mode.
costs: The cost (in dollars) to traverse a single block using each mode.
Movement is allowed up, down, left, and right. You may only travel along contiguous cells of the same transportation mode (i.e., same digit). You cannot move between cells of different modes, nor can you cross roadblocks.

For each mode i, the time and cost to traverse a single block are given by times[i] and costs[i], respectively. The total travel time and cost are calculated as the sum of the time and cost for each cell visited along the path from 'S' to 'D'.

Return the name of the transportation mode that yields the minimum total time from 'S' to 'D'. If multiple modes result in the same minimum time, return the one with the lowest total cost. Return an empty string if no valid route exists.

Constraints:

1 ≤ grid.length, grid[0].length ≤ 100
Exactly one 'S' and one 'D' exist.
modes.length ≤ 10
costs[i], times[i] are non-negative integers.
Example 1

Input:
grid = [["3", "3", "S", "2", "X", "X"],
        ["3", "1", "1", "2", "X", "2"],
        ["3", "1", "1", "2", "2", "2"],
        ["3", "1", "1", "1", "D", "3"],
        ["3", "3", "3", "3", "3", "4"],
        ["4", "4", "4", "4", "4", "4"]],
modes = ["Walk", "Bike", "Car", "Train"],
costs = [0, 1, 3, 2],
times = [3, 2, 1, 1]

Output: "Bike"

Explanation: The optimal path stays on mode "2" (Bike). One possible route from "S" at (0,2) → (0,3) → (1,3) → (2,3) → (3,3) → "D" at (3,4) traverses 5 bike-blocks.

Total time = 5 × 2 min = 10 min
Total cost = 5 × $1 = $5
Other modes either cannot reach 'D' continuously or yield higher time/cost.

Example 2

Input:
grid = [["S", "1", "1"],
        ["2", "2", "2"],
        ["D", "1", "1"]],
modes = ["Walk", "Bike", "Car", "Train"],
costs = [0, 1, 3, 2],
times = [2, 2, 1, 1]

Output: "Bike"

Example 3

Input:
grid = [["S", "1", "X"],
        ["X", "3", "3"],
        ["2", "2", "D"]],
modes = ["Walk", "Bike", "Car"],
costs = [0, 1, 3, 2],
times = [3, 2, 1, 1]

Output: ""

