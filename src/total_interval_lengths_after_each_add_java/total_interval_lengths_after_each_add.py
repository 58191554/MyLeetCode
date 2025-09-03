from typing import List

def total_lengths_after_each_add(ops: List[List[int]]):
    intervals: List[List[int]] = []  # disjoint, sorted by start
    total_len = 0
    ans: List[int] = []

    for start, end in ops:
        new_l, new_r = start, end
        n = len(intervals)
        i = 0

        # Skip intervals entirely before the new one (no adjacency) using binary search on ends
        if n > 0:
            def _first_ge(arr, target):
                l, r = 0, len(arr)
                while l < r:
                    m = (l + r) // 2
                    if arr[m] < target:
                        l = m + 1
                    else:
                        r = m
                return l

            ends = [iv[1] for iv in intervals]
            i = _first_ge(ends, new_l - 1)

        # Merge all overlapping or adjacent intervals and accumulate removed length
        j = i
        removed = 0
        while j < n and intervals[j][0] <= new_r + 1:
            removed += intervals[j][1] - intervals[j][0] + 1
            if intervals[j][0] < new_l:
                new_l = intervals[j][0]
            if intervals[j][1] > new_r:
                new_r = intervals[j][1]
            j += 1

        # Replace merged range
        intervals[i:j] = [[new_l, new_r]]

        # Update total covered length
        total_len = total_len - removed + (new_r - new_l + 1)
        ans.append(total_len)

    return ans