import pytest
from cidr_white_checklist import Solution


def test_basic_true_false():
    sol = Solution()
    cidrs = ["192.168.0.0/16", "10.0.0.0/8"]
    assert sol.cidr_white_checklist(cidrs, "192.168.1.23") is True
    assert sol.cidr_white_checklist(cidrs, "172.16.0.1") is False


def test_network_and_broadcast_included():
    sol = Solution()
    cidrs = ["192.168.1.0/24"]
    # network address
    assert sol.cidr_white_checklist(cidrs, "192.168.1.0") is True
    # broadcast address
    assert sol.cidr_white_checklist(cidrs, "192.168.1.255") is True


def test_multiple_cidrs_any_match():
    sol = Solution()
    cidrs = ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
    assert sol.cidr_white_checklist(cidrs, "172.20.10.5") is True
    assert sol.cidr_white_checklist(cidrs, "8.8.8.8") is False


def test_prefix_zero_matches_all():
    sol = Solution()
    cidrs = ["0.0.0.0/0"]
    assert sol.cidr_white_checklist(cidrs, "0.0.0.0") is True
    assert sol.cidr_white_checklist(cidrs, "255.255.255.255") is True
    assert sol.cidr_white_checklist(cidrs, "8.8.8.8") is True
