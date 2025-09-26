from typing import Dict, List, Iterator, Optional

class Entry:
    def __init__(self, value: int, birth: int):
        self.value: int = value
        self.birth: int = birth  # inclusive
        self.death: int = float('inf')  # exclusive
        self.nx = None
        self.pv = None

    def aliveAt(self, v: int) -> bool:
        return self.birth <= v < self.death

class SnapshotSet:
    def __init__(self):
        # 双哨兵
        self.head = Entry(0, 0)
        self.tail = Entry(0, 0)
        self.head.nx = self.tail
        self.tail.pv = self.head

        self.cur = 0
        self.alive_mp: Dict[int, Entry] = {}
        self.activeSnaps: List[int] = []

    def add(self, n: int) -> bool:
        if n in self.alive_mp:
            return False
        self.cur += 1
        e = Entry(n, self.cur)
        self.alive_mp[n] = e
        # 插到 tail 前
        end = self.tail.pv
        end.nx = e
        e.pv = end
        e.nx = self.tail
        self.tail.pv = e
        return True

    def remove(self, n: int) -> bool:
        e = self.alive_mp.get(n)
        if e is None:
            return False
        self.cur += 1
        e.death = self.cur
        self.alive_mp.pop(n)
        return True

    def contains(self, n: int) -> bool:
        return n in self.alive_mp

    def getIterator(self) -> Iterator[int]:
        snap = self.cur
        self.activeSnaps.append(snap)
        return self.SnapshotIterator(self, snap)

    class SnapshotIterator:
        def __init__(self, outer: 'SnapshotSet', v: int):
            self.outer = outer
            self.version = v
            self.tail = outer.tail
            self.cur: Optional[Entry] = outer.head.nx  # 第一个真实节点

        def __iter__(self) -> 'SnapshotSet.SnapshotIterator':
            return self

        def __next__(self) -> int:
            if not self.hasNext():
                # 耗尽：注销快照并 GC
                try:
                    self.outer.activeSnaps.remove(self.version)
                except ValueError:
                    pass
                self.outer._gc()
                raise StopIteration
            val = self.cur.value
            self.cur = self.cur.nx
            return val

        def hasNext(self) -> bool:
            node = self.cur
            if node is None:  # 保护：应对极端情况
                return False
            # 找到第一个对本快照可见的节点；遇到未来出生的可提前结束
            while node != self.tail:
                if node.birth > self.version:
                    break
                if node.aliveAt(self.version):
                    self.cur = node
                    return True
                node = node.nx
                if node is None:  # 若外部回收破坏了链式可达，防御返回
                    return False
            self.cur = node
            return False

    # 丢弃所有“对最老活跃快照也不可见”的链表前缀
    def _gc(self) -> None:
        oldest = self.cur if not self.activeSnaps else min(self.activeSnaps)
        node = self.head.nx
        while node != self.tail and node.death < oldest:
            nxt = node.nx
            # 物理摘除：让 head 指向 nxt，nxt 的 pv 指回 head
            self.head.nx = nxt
            nxt.pv = self.head
            # ⚠️ 关键：不要把 node.nx 置空，避免正在迭代的游标失联
            # 允许把回指断开以便更快释放
            node.pv = None
            # （node 仍可能被某个迭代器引用；当引用解除后，Python GC 会释放）
            node = nxt

# Helper function to iterate all elements in the iterator for easier visualization
def iterateAllElements(it: Iterator[int]) -> List[int]:
    return list(it)

def test1():
    print("======== test 1: =========")
    s = SnapshotSet()
    assert s.add(1) is True
    assert s.add(2) is True
    assert s.add(3) is True
    assert s.add(4) is True
    assert s.add(1) is False
    it1 = s.getIterator()
    assert s.remove(1) is True
    assert s.remove(3) is True
    assert s.remove(5) is False
    it2 = s.getIterator()
    assert iterateAllElements(it1) == [1, 2, 3, 4]
    assert iterateAllElements(it2) == [2, 4]
    print("======== test 1: passed =========")
def test2():
    print("======== test 2: =========")
    s = SnapshotSet()
    it1 = s.getIterator()
    assert s.add(10) is True
    it2 = s.getIterator()
    assert s.add(20) is True
    it3 = s.getIterator()
    assert s.add(30) is True
    it4 = s.getIterator()
    assert s.remove(30) is True
    it5 = s.getIterator()
    assert s.remove(20) is True
    it6 = s.getIterator()
    assert s.remove(10) is True
    it7 = s.getIterator()

    assert iterateAllElements(it1) == []
    assert iterateAllElements(it2) == [10]
    assert iterateAllElements(it3) == [10, 20]
    assert iterateAllElements(it4) == [10, 20, 30]
    assert iterateAllElements(it5) == [10, 20]
    assert iterateAllElements(it6) == [10]
    assert iterateAllElements(it7) == []
    print("======== test 2: passed =========")

def test3():
    print("======== test 3: =========")
    s = SnapshotSet()
    assert s.remove(5) is False
    assert s.add(5) is True
    assert s.remove(5) is True
    assert s.add(5) is True
    assert iterateAllElements(s.getIterator()) == [5]
    print("======== test 3: passed =========")
def test4():
    print("======== test 4: =========")
    s = SnapshotSet()
    assert s.add(1) is True
    assert s.add(2) is True
    assert s.add(3) is True
    assert s.add(4) is True
    assert s.add(5) is True
    it1 = s.getIterator()
    assert s.remove(2) is True
    assert s.remove(4) is True
    assert s.add(6) is True
    it2 = s.getIterator()
    assert iterateAllElements(it1) == [1, 2, 3, 4, 5]
    assert iterateAllElements(it2) == [1, 3, 5, 6]
    print("======== test 4: passed =========")

if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
