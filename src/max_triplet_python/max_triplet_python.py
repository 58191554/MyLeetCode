from typing import List

def maxTriplets(nums: List[int]) -> int:
    n = len(nums)
    if n < 3:
        return 0
    cache = [0] * (n + 1)
    for i in range(n - 3, -1, -1):
        if nums[i] + nums[i + 1] + nums[i + 2] == 0:
            cache[i] = max([1 + cache[i + 3], cache[i + 1], cache[i + 2]])
        else:
            cache[i] = max([cache[i + 1], cache[i + 2], cache[i + 3]])
    return max(cache[0], cache[1], cache[2])