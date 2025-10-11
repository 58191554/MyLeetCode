from math import inf
import heapq
from typing import List

def sortedSplitMergeCount(nums: List[int]) -> int:
    n = len(nums)
    surfixMin = [0] * n
    surfixMin[-1] = nums[-1]
    for i in range(n - 2, -1, -1):
        surfixMin[i] = min(surfixMin[i + 1], nums[i])
    leftMax = nums[0]
    result = 0
    for i in range(1, n):
        if leftMax <= surfixMin[i]:
            result += 1
        leftMax = max(leftMax, nums[i])
    return result