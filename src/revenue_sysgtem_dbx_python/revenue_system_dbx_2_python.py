from typing import List, Optional
from sortedcontainers import SortedSet

class Customer:
    def __init__(self, user_id: int, revenue: int):
        self.revenue = revenue
        self.user_id = user_id
        self.parent = None
        self.children = []
    def __lt__(self, o):
        assert isinstance(o, Customer)
        if self.revenue == o.revenue:
            return self.user_id < o.user_id
        return self.revenue < o.revenue
    def __hash__(self):
        return hash("customer:{}".format(self.user_id))
    def __eq__(self, o):
        assert isinstance(o, Customer)
        return self.user_id == o.user_id and self.revenue == o.revenue
        
class RevenueSystem:
    def __init__(self, ):
        self.sorted_set = SortedSet()
        self.customer_mp = dict()
        self.nx_user_id = 0
        
    def add(self, revenue: int) -> int:
        c = Customer(self.nx_user_id, revenue)
        self.sorted_set.add(c)
        self.customer_mp[c.user_id] = c
        self.nx_user_id += 1
        return c.user_id

    def addByReferral(self, revenue: int, referrerId: int) -> int:
        if referrerId not in self.customer_mp:
            return -1
        ref = self.customer_mp[referrerId]
        assert ref is not None
        assert ref in self.sorted_set
        self.sorted_set.remove(ref)
        c = Customer(self.nx_user_id, revenue)
        c.parent = ref
        ref.children.append(c)
        self.nx_user_id += 1
        self.customer_mp[c.user_id] = c
        self.sorted_set.add(c)
        ref.revenue += revenue
        self.sorted_set.add(ref)
        return c.user_id

    def getTopKCustomer(self, k: int, minRevenue: int) -> List[int]:
        result = []
        n = len(self.sorted_set)
        for i in range(min(n, k)):
            c = self.sorted_set[n - 1 - i]
            if c.revenue < minRevenue:
                return result
            result.append(c.user_id)
        return result

    def getReferer(self, userId: int) -> int:
        if userId not in self.customer_mp:
            return -1
        c = self.customer_mp[userId]
        assert c is not None
        assert c in self.sorted_set
        if c.parent is None:
            return -1
        return c.parent.user_id

    def getChildren(self, userId: int) -> List[int]:
        if userId not in self.customer_mp:
            return []
        c = self.customer_mp[userId]
        assert c is not None
        assert c in self.sorted_set
        return [child.user_id for child in c.children]