import math

class VNode:
    def __init__(self, val, birth):
        self.val = val
        self.birth = birth
        self.death = math.inf
        self.pv, self.nx = None, None
    
    def __repr__(self):
        return str(self.val) + "[birth = " + str(self.birth) + ", death = " + str(self.death) + "]"
class SnapshotSet:
    def __init__(self):
        self.clock = 0
        self.mp = dict()
        self.mp["head"] = VNode(None, 0)
        self.mp["tail"] = VNode(None, 0)
        self.mp["tail"].pv, self.mp["head"].nx = self.mp["head"], self.mp["tail"]
        
    def add(self, n: int) -> bool:
        if n in self.mp: return False
        nd = VNode(n, self.clock)
        self.clock += 1
        tl = self.mp["tail"]
        pv = tl.pv
        pv.nx = nd; nd.pv = pv
        nd.nx = tl; tl.pv = nd
        self.mp[n] = nd
        return True

    def remove(self, n: int) -> bool:
        if n not in self.mp:
            return False
        nd = self.mp[n]
        nd.death = self.clock
        self.clock += 1
        self.mp.pop(n)
        return True

    def getIterator(self):
        ss = SnapshotIterator(self, self.clock)
        ss.cur = self.mp["head"].nx
        self.clock += 1
        return ss

class SnapshotIterator:
    def __init__(self, s: SnapshotSet, snap: int):
        self.cur = None
        self.snap = snap

    def __iter__(self):
        return self

    def __next__(self):
        if self.cur is None:
            raise StopIteration
        while self.cur:
            candidate = self.cur
            self.cur = self.cur.nx
            if candidate and candidate.val != None and candidate.birth <= self.snap < candidate.death:
                return candidate.val
        raise StopIteration