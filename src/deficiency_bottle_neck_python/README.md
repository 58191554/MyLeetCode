Find Defendency Bottleneck
Medium
Breadth First Search
Interview Stages
Screening
Frequency
Asked By


Last Reported
2 weeks ago
Given n dependencies labeled from 0 to n - 1, and a list of acyclic edges edges, where each pair [u, v] indicates that dependency v depends on the build completion of dependency u, identify all bottleneck dependencies.

A dependency is considered a bottleneck if, at any time step, it is the only one being built. Each dependency takes exactly one time unit to build and can start immediately after all its prerequisites have been completed. Multiple dependencies may be built in parallel if they are ready.

Return a list of all dependencies that act as bottlenecks, and you may return the result in any order.

Constraints:

1 <= n <= 10⁵
The dependencies are acyclic.
Example 1:


Input: n = 5, edges = [[0, 1], [0, 2], [1, 3], [1, 4]]
Output: [0]
Explanation: Only dependency 0 must be built individually. Dependencies 1 and 2, as well as 3 and 4, can be built in parallel.

Example 2:

Input: n = 4, edges = [[0, 1], [1, 2], [2, 3]]
Output: [0, 1, 2, 3]

Example 3:

Input: n = 6, edges = [[0, 1], [2, 3], [4, 5]]
Output: []

