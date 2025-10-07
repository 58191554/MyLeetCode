import math

class Entry:
    def __init__(self, value: int, birth: int):
        self.value = value
        self.birth = birth
        self.death = math.inf

    def aliveAt(self, t: int) -> bool:
        return self.birth <= t < self.death
class SnapshotSet:
    def __init__(self):
        self.log = []
        self.entryMp = dict()
        self.aliveSnap = []
        self.version = 0
        self.gcIdx = 0

    def add(self, n: int) -> bool:
        if n in self.entryMp:
            return False
        entry = Entry(n, birth=self.version)
        self.log.append(entry)
        self.entryMp[n] = entry
        self.version += 1
        return True

    def remove(self, n: int) -> bool:
        if n not in self.entryMp:
            return False
        entry = self.entryMp.pop(n)
        entry.death = self.version
        return True
        
    def contains(self, n: int) -> bool:
        return n in self.entryMp
    
    def getIterator(self):
        snapshotset_iter = SnapshotSetIterator(self, self.version)
        self.aliveSnap.append(self.version)
        self.version += 1
        return snapshotset_iter
        
    def gc(self, snap_version):
        if snap_version == min(self.aliveSnap):
            self.aliveSnap.remove(snap_version)
            if not self.aliveSnap:
                self.gcIdx = len(self.log)
            else:
                oldest_version = min(self.aliveSnap)
                while self.gcIdx < len(self.log):
                    if self.log[self.gcIdx].aliveAt(oldest_version):
                        break
                    else:
                        self.gcIdx += 1
        else:
            self.aliveSnap.remove(snap_version)

class SnapshotSetIterator:
    def __init__(self, outer, version):
        self.version = version
        self.outer = outer
        self.cur = outer.gcIdx
        self.log = outer.log
    
    def __iter__(self):
        return self
    
    def __next__(self):
        while self.cur < len(self.log):
            if self.log[self.cur].aliveAt(self.version):
                result = self.log[self.cur].value
                self.cur += 1
                return result
            self.cur += 1
        self.outer.gc(self.version)
        raise StopIteration

    def hasNext(self):
        while self.cur < len(self.log):
            if self.log[self.cur].aliveAt(self.version):
                return True
            self.cur += 1
        self.outer.gc(self.version)
        return False
