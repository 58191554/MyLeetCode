
from sortedcollections import SortedSet
from typing import Optional, Tuple
class Bid:
    def __init__(self, bid_id, price, product_id):
        self.bid_id = bid_id
        self.price = price
        self.product_id = product_id
    def __lt__(self, o):
        if self.price == o.price:
            return self.bid_id < o.bid_id
        return self.price < o.price
    def __hash__(self):
        return hash(self.bid_id)
    def __eq__(self, o):
        return self.bid_id == o.bid_id
    def __repr__(self):
        return f"Bid(bid_id={self.bid_id}, price={self.price}, product_id={self.product_id})"

class Bids:
    def __init__(self, ):
        self.productDict = dict()
        self.idToBid = dict()
        
    def addBid(self, bid_id: int, product_id: int, price: int) -> None:
        self.productDict.setdefault(product_id, SortedSet())
        if bid_id in self.idToBid:
            bid = self.idToBid[bid_id]
            self.productDict[bid.product_id].remove(bid)
            bid.price = price
            bid.product_id = product_id
        else:
            bid = Bid(bid_id=bid_id, price=price, product_id=product_id)
            self.idToBid[bid_id] = bid
        self.productDict[product_id].add(bid)
        
    def removeBid(self, bid_id: int) -> bool:
        if bid_id not in self.idToBid:
            return False
        bid = self.idToBid[bid_id]
        self.idToBid.pop(bid_id)
        product_id = bid.product_id
        self.productDict[product_id].remove(bid)
        return True

    def queryClosestBid(self, product_id: int, price: int) -> Optional[Tuple[int, int]]:
        if product_id not in self.productDict or not self.productDict[product_id]:
            return None
        sortedset = self.productDict[product_id]
        print("sortedset:", sortedset)
        def binarySearch(x):
            l, r = 0, len(sortedset)
            while l < r:
                mid = (l + r) // 2
                if sortedset[mid].price < x:
                    l = mid + 1
                else:
                    r = mid
            return l
        first_ge = binarySearch(price)
        result = None
        if first_ge == len(sortedset):
            result = sortedset[-1]
        elif first_ge == 0:
            result = sortedset[0]
        else:
            p1 = sortedset[first_ge].price
            p2 = sortedset[first_ge - 1].price
            if abs(p1 - price) < abs(p2 - price):
                result = sortedset[first_ge]
            elif abs(p1 - price) > abs(p2 - price):
                result = sortedset[first_ge - 1]
            else:
                result = sortedset[first_ge - 1]
        return result.bid_id, result.price
    
# if __name__ == "__main__":
#     bids = Bids()
#     bids.addBid(101, 7, 500)
#     bids.addBid(102, 7, 520)
#     bids.addBid(103, 7, 480)
#     bids.addBid(201, 8, 1000)
#     print(bids.queryClosestBid(7, 510))