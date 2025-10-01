from typing import List, Optional

class Solution:
    def deleteCoveredPoint(self, intervals: List[List[int]], idx: int) -> List[List[int]]:
        cur = 0
        for i, (l, r) in enumerate(intervals):
            size = r - l
            if cur <= idx < cur + size:
                if cur == idx:
                    if size == 1:
                        intervals = intervals[:i] + intervals[i + 1:]
                    else:
                        intervals[i] = [l + 1, r]
                elif cur + size - 1 == idx:
                    intervals[i] = [l, r - 1]
                else:
                    pop_idx = idx - cur
                    left = [l, l + pop_idx]
                    right = [l + pop_idx + 1, r]
                    intervals = intervals[:i] + [left, right] + intervals[i + 1:]
                break
            cur += size
        return intervals
        
                    