import sys
from pathlib import Path

import pytest

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from bids_of_product_python.bids_of_product_python_ref import Bids


def test_query_closest_bid_uses_price_then_id_tiebreaks():
    bids = Bids()
    bids.addBid(101, 7, 500)
    bids.addBid(102, 7, 520)
    bids.addBid(103, 7, 480)
    bids.addBid(201, 8, 1000)
    # same diff of 10 between 500 and 520 – lower price wins
    assert bids.queryClosestBid(7, 510) == (101, 500)

    # add another bid at price 500 but larger id – smaller id still wins
    bids.addBid(150, 7, 500)
    assert bids.queryClosestBid(7, 500) == (101, 500)


def test_remove_bid_and_empty_product_state():
    bids = Bids()
    bids.addBid(301, 9, 300)
    bids.addBid(302, 9, 400)
    assert bids.queryClosestBid(9, 350) == (301, 300)

    assert bids.removeBid(301) is True
    assert bids.queryClosestBid(9, 350) == (302, 400)

    assert bids.removeBid(999) is False

    assert bids.removeBid(302) is True
    assert bids.queryClosestBid(9, 350) is None


def test_updating_existing_bid_moves_between_products():
    bids = Bids()
    bids.addBid(1, 1, 100)
    bids.addBid(2, 1, 110)
    assert bids.queryClosestBid(1, 105) == (1, 100)

    bids.addBid(1, 2, 200)  # update bid 1 to new product and price
    assert bids.queryClosestBid(1, 105) == (2, 110)
    assert bids.queryClosestBid(2, 199) == (1, 200)
