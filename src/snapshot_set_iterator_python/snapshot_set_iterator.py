from math import inf
import heapq
from collections import deque
class Entry:
    def __init__(self, val, birth):
        self.val = val
        self.birth = birth; self.death = inf
        
    def alive(self, time):
        return self.birth <= time < self.death

class SnapshotSet:
    def __init__(self):
        self.log = []
        self.mp = {}
        self.alive_snap_versions = []
        self.alive_heap = []
        self.version = 0
        self.gcIdx = 0

    def add(self, n: int) -> bool:
        if n in self.mp:
            return False
        entry = Entry(n, self.version)
        self.mp[n] = entry
        self.log.append(entry)
        return True

    def remove(self, n: int) -> bool:
        if n not in self.mp:
            return False
        entry = self.mp.pop(n)
        entry.death = self.version
        return True
        
    def contains(self, n: int) -> bool:
        return n in self.mp
    
    def getIterator(self):
        snapshotSetItr = SnapshotSetIterator(self, self.version)
        self.alive_snap_versions.append(self.version)
        heapq.heappush(self.alive_heap, self.version)
        self.version += 1
        return snapshotSetItr
    
    def gc(self, stale_version):
        if not self.alive_snap_versions:
            return
        self.alive_snap_versions.remove(stale_version)
        if self.alive_heap and self.alive_heap[0] == stale_version:
            while self.alive_heap and self.alive_heap[0] not in self.alive_snap_versions:
                heapq.heappop(self.alive_heap)
        oldest_version = self.alive_heap[0] if self.alive_heap else self.version
        while self.gcIdx < len(self.log) and self.log[self.gcIdx].death <= oldest_version:
            self.gcIdx += 1

class SnapshotSetIterator:
    def __init__(self, outer, version):
        self.outer = outer
        self.curIdx = outer.gcIdx
        self.version = version
        
    def __next__(self):
        log = self.outer.log
        while self.curIdx < len(log):
            if not log[self.curIdx].alive(self.version):
                self.curIdx += 1
                continue
            result = log[self.curIdx].val
            self.curIdx += 1
            return result
        self.outer.gc(self.version)
        raise StopIteration
    
    def __iter__(self):
        return self

    def has_next(self):
        log = self.outer.log
        while self.curIdx < len(log):
            if not log[self.curIdx].alive(self.version):
                self.curIdx += 1
            else:
                return True
        self.outer.gc(self.version)
        return False
