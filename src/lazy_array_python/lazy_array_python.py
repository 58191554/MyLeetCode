class FuncNode:
    def __init__(self, func):
        self.prev = None
        self.func = func
        self.cache = None

class LazyArray:
    def __init__(self, arr, functions=None):
        self.arr = arr
        self.funcNode = FuncNode(functions)

    def map(self, fn):
        la = LazyArray(self.arr, fn)
        la.funcNode.prev = self.funcNode
        return la

    def indexOf(self, target):
        func = self.funcNode.cache or self.getFunc()
        for i, x in enumerate(self.arr):
            if func(x) == target:
                return i
        return -1

    def getFunc(self):
        stk = []
        tmp = self.funcNode
        # 收集到“最近的已缓存节点”或 None
        while tmp is not None and tmp.cache is None:
            stk.append(tmp)
            tmp = tmp.prev

        # 基底：已缓存的组合函数，或者恒等
        base = (tmp.cache if (tmp is not None and tmp.cache is not None) else (lambda x: x))

        # 按从旧到新组合： base = f ∘ base
        while stk:
            node = stk.pop()
            if node.func is not None:
                f = node.func
                prev_base = base
                base = (lambda x, f=f, prev_base=prev_base: f(prev_base(x)))

        # 把组合结果缓存到当前节点
        self.funcNode.cache = base
        return base
