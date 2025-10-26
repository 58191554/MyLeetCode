from typing import Optional, Tuple


class Bids:
    def addBid(self, bid_id: int, product_id: int, price: int) -> None:
        ...

    def removeBid(self, bid_id: int) -> bool:
        ...

    def queryClosestBid(self, product_id: int, price: int) -> Optional[Tuple[int, int]]:
        ...
