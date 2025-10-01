Remove Covered Point
Medium
Array
Interview Stages
Onsite
Frequency
Asked By

Last Reported
4 days ago
You are given a list of non-overlapping intervals, where each interval [start, end] represents a range of integers from start (inclusive) to end (exclusive). For example, the interval [10, 13] covers the integers 10, 11, and 12. These intervals collectively cover a sequence of integer points.

You are also given an integer idx, which refers to the index (0-based) of a point you need to remove, in the flattened sequence of all covered integers ordered according to the input intervals.

Removing a single point may:

Eliminate an interval if it contains only that point.
Shrink an interval by adjusting its boundary.
Split an interval into two non-overlapping parts.
Return the updated list of intervals representing the remaining points after you remove the integer at position idx from this sequence, and your result should preserve the original order for any intervals that are unchanged or partially modified.

Constraints:

1 ≤ intervals.length ≤ 10⁴
0 ≤ intervals[i][0] < intervals[i][1] ≤ 10⁹
Example 1:

Input: intervals = [[10, 12], [13, 16], [4, 8]], idx = 3
Output: [[10, 12], [13, 14], [15, 16], [4, 8]]
Explanation: The covered points are [10, 11, 13, 14, 15, 4, 5, 6, 7]. Point 14 (at index 3) will be removed. After removal, the covered points become [10, 11, 13, 15, 4, 5, 6, 7], resulting in the updated intervals: [[10, 12], [13, 14], [15, 16], [4, 8]].

Example 2:

Input: intervals = [[4, 8], [13, 16], [10, 12]], idx = 0
Output: [[5, 8], [13, 16], [10, 12]]

Example 3:

Input: intervals = [[2, 6], [8, 10], [15, 18]], idx = 3
Output: [[2, 5], [8, 10], [15, 18]]