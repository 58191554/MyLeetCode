from typing import List, Optional

class Solution:
    def findPath(self, order: int, source: int, dest: int) -> str:
        if source == dest:
            return ""
        fibs = [1, 1]
        for i in range(2, order + 1):
            fibs.append(fibs[-1] + fibs[-2] + 1)
        def getBoundaries(x, o):
            assert o >= 2
            l_size, r_size = fibs[o - 2], fibs[o - 1]
            l_start = x + 1
            l_end = l_start + l_size - 1
            r_start = l_end + 1
            r_end = r_start + r_size - 1
            return l_start, l_end, r_start, r_end
            
        def findCommonParent(x, o):
            if x == source or x == dest:
                return (x, o)
            l_start, l_end, r_start, r_end = getBoundaries(x, o)
            if l_start <= source <= l_end and l_start <= dest <= l_end:
                return findCommonParent(l_start, o - 2)
            if r_start <= source <= r_end and r_start <= dest <= r_end:
                return findCommonParent(r_start, o - 1)
            return (x, o)
        cp_x, cp_o = findCommonParent(0, order)
        def findSourcePath(x, o):
            if x == source:
                return ""
            path = ""
            l_start, l_end, r_start, r_end = getBoundaries(x, o)
            if l_start <= source <= l_end:
                path += findSourcePath(l_start, o - 2)
            else:
                path += findSourcePath(r_start, o - 1)
            path += "U"
            return path
        
        def findDestPath(x, o):
            if x == dest:
                return ""
            path = ""
            l_start, l_end, r_start, r_end = getBoundaries(x, o)
            if l_start <= dest <= l_end:
                path += "L"
                path += findDestPath(l_start, o - 2)
            else:
                path += "R"
                path += findDestPath(r_start, o - 1)
            return path
        return findSourcePath(cp_x, cp_o) + findDestPath(cp_x, cp_o)
