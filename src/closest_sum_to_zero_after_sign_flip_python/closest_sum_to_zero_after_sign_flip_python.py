from typing import List

def closest_sum_to_zero_after_sign_flip_python(nums: List[int]):
    numsSum = sum(nums)
    result = abs(numsSum)
    for x in nums:
        tmp = numsSum - 2 * x
        result = min(abs(tmp), result)
    return result