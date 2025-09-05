from typing import Dict, List, Iterator, Optional

class Entry:
    def __init__(self, value: int, birth: int):
        self.value: int = value
        self.birth: int = birth  # inclusive
        self.death: int = float('inf')  # exclusive

    def aliveAt(self, v: int) -> bool:
        return self.birth <= v < self.death

class SnapshotSet:
    def __init__(self):
        self.logHistory: List[Entry] = []  # append-only history
        self.liveEntryMap: Dict[int, Entry] = {}  # currently present values
        self.activeSnaps: List[int] = []  # For gc support

        self.version: int = 0  # global logical clock
        self.gcIndex: int = 0  # First entry that may still be needed by any iterator

    def add(self, n: int) -> bool:
        if n in self.liveEntryMap:
            return False
        self.version += 1
        entry = Entry(n, self.version)
        self.logHistory.append(entry)
        self.liveEntryMap[n] = entry
        return True

    def remove(self, n: int) -> bool:
        entry = self.liveEntryMap.get(n)
        if entry is None:
            return False
        self.version += 1
        entry.death = self.version
        del self.liveEntryMap[n]
        return True

    def contains(self, n: int) -> bool:
        return n in self.liveEntryMap

    def getIterator(self) -> Iterator[int]:
        self.activeSnaps.append(self.version)
        return self.SnapshotIterator(self, self.version)

    class SnapshotIterator:
        def __init__(self, outer: 'SnapshotSet', snap: int):
            self.outer = outer
            self.snap: int = snap  # Fixed version this iterator sees
            self.idx: int = outer.gcIndex  # We never need to scan earlier than gcIndex
            self.next: Optional[int] = None  # Cached next element
            self._advance()

        def __iter__(self) -> 'SnapshotSet.SnapshotIterator':
            return self

        def __next__(self) -> int:
            if self.next is None:
                raise StopIteration
            res = self.next
            self._advance()
            return res

        def hasNext(self) -> bool:
            return self.next is not None

        # Advances to the next visible entry in the log history for this snapshot.
        def _advance(self) -> None:
            self.next = None
            while self.idx < len(self.outer.logHistory):
                entry = self.outer.logHistory[self.idx]
                self.idx += 1
                if entry.aliveAt(self.snap):
                    # visible in this snapshot
                    self.next = entry.value
                    return

            # Exhausted, drop snapshot and try to GC
            try:
                self.outer.activeSnaps.remove(self.snap)
            except ValueError:
                pass
            self.outer._gc()

    # Discards history that no active iterator can reach.
    def _gc(self) -> None:
        oldestSnap = self.version if not self.activeSnaps else min(self.activeSnaps)
        while (self.gcIndex < len(self.logHistory) and
               self.logHistory[self.gcIndex].death < oldestSnap):
            self.gcIndex += 1 # entry is invisible to every live iterator

