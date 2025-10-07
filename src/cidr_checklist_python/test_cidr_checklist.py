import pytest
from cidr_checklist import Solution


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

def test_prefix_32_matches_all():
    sol = Solution()
    cidrs = ["0.0.0.0/32"]
    assert sol.cidr_white_checklist(cidrs, "0.0.0.0") is True
    assert sol.cidr_white_checklist(cidrs, "255.255.255.255") is True
    assert sol.cidr_white_checklist(cidrs, "8.8.8.8") is True


def test_boundary_addresses_various_prefixes():
    sol = Solution()
    # /24 boundaries
    cidrs = ["10.0.1.0/24"]
    assert sol.cidr_white_checklist(cidrs, "10.0.1.0") is True
    assert sol.cidr_white_checklist(cidrs, "10.0.1.255") is True
    assert sol.cidr_white_checklist(cidrs, "10.0.2.0") is False
    # /31 includes exactly two addresses
    cidrs = ["192.168.1.10/31"]
    assert sol.cidr_white_checklist(cidrs, "192.168.1.10") is True
    assert sol.cidr_white_checklist(cidrs, "192.168.1.11") is True
    assert sol.cidr_white_checklist(cidrs, "192.168.1.12") is False
    # /32 exact host
    cidrs = ["203.0.113.42/32"]
    assert sol.cidr_white_checklist(cidrs, "203.0.113.42") is True
    assert sol.cidr_white_checklist(cidrs, "203.0.113.43") is False


def test_overlapping_cidrs_first_match_wins_behavior():
    sol = Solution()
    # Smaller prefix area listed earlier should be decisive
    cidrs = ["192.168.1.128/25", "192.168.1.0/24"]
    assert sol.cidr_white_checklist(cidrs, "192.168.1.200") is True
    assert sol.cidr_white_checklist(cidrs, "192.168.1.100") is True


def test_extreme_addresses_and_large_prefix():
    sol = Solution()
    cidrs = ["255.255.255.255/32", "0.0.0.0/1"]
    assert sol.cidr_white_checklist(cidrs, "255.255.255.255") is True
    assert sol.cidr_white_checklist(cidrs, "127.255.255.255") is True
    assert sol.cidr_white_checklist(cidrs, "128.0.0.0") is False


def test_empty_cidr_list_returns_false():
    sol = Solution()
    cidrs = []
    assert sol.cidr_white_checklist(cidrs, "1.2.3.4") is False


# --- LeetCode-style operations tests for IpFirewall ---

def _ip_to_int(ip: str) -> int:
    a, b, c, d = map(int, ip.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d


def _matches(ip: str, cidr: str) -> bool:
    if "/" not in cidr:
        return _ip_to_int(ip) == _ip_to_int(cidr)
    base, prefix = cidr.split("/")
    prefix = int(prefix)
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF if prefix > 0 else 0
    ip_i = _ip_to_int(ip)
    net = _ip_to_int(base) & mask
    return (ip_i & mask) == net


class IpFirewall:
    def __init__(self, rules):
        self.rules = rules

    def allowAccess(self, ip: str) -> bool:
        for action, cidr in self.rules:
            if _matches(ip, cidr):
                return action == "ALLOW"
        return False


def _execute_ops(ops, args):
    res = []
    fw = None
    for op, arg in zip(ops, args):
        if op == "IpFirewall":
            fw = IpFirewall(arg[0])
            res.append(None)
        elif op == "allowAccess":
            res.append(fw.allowAccess(arg[0]))
        else:
            raise ValueError(f"Unknown op {op}")
    return res


def test_ops_example_1():
    ops = ["IpFirewall", "allowAccess", "allowAccess", "allowAccess", "allowAccess"]
    args = [
        [[
            ["ALLOW", "192.168.1.100"],
            ["DENY", "192.168.1.0/24"],
            ["ALLOW", "192.168.0.0/16"],
            ["DENY", "0.0.0.0/0"],
        ]],
        ["192.168.1.100"],
        ["192.168.1.50"],
        ["192.168.2.10"],
        ["10.0.0.1"],
    ]
    expected = [None, True, False, True, False]
    assert _execute_ops(ops, args) == expected


def test_ops_example_2():
    ops = ["IpFirewall", "allowAccess", "allowAccess", "allowAccess"]
    args = [
        [[
            ["DENY", "10.0.0.0/16"],
            ["ALLOW", "10.0.1.0/24"],
            ["DENY", "0.0.0.0/0"],
        ]],
        ["10.0.1.50"],
        ["10.0.2.10"],
        ["192.168.1.1"],
    ]
    expected = [None, False, False, False]
    assert _execute_ops(ops, args) == expected


def test_ops_example_3():
    ops = ["IpFirewall", "allowAccess", "allowAccess", "allowAccess"]
    args = [
        [[
            ["ALLOW", "172.16.0.0/12"],
            ["DENY", "172.20.0.0/16"],
            ["ALLOW", "172.20.5.0/24"],
            ["DENY", "0.0.0.0/0"],
        ]],
        ["172.18.1.1"],
        ["172.20.1.1"],
        ["172.20.5.10"],
    ]
    expected = [None, True, True, True]
    assert _execute_ops(ops, args) == expected


def test_ops_example_4():
    ops = [
        "IpFirewall",
        "allowAccess",
        "allowAccess",
        "allowAccess",
        "allowAccess",
        "allowAccess",
        "allowAccess",
        "allowAccess",
    ]
    args = [
        [[
            ["ALLOW", "10.0.0.1"],
            ["DENY", "10.0.0.0/24"],
            ["ALLOW", "10.0.0.0/16"],
            ["DENY", "0.0.0.0/0"],
            ["ALLOW", "192.168.1.0/24"],
            ["ALLOW", "172.16.0.0/12"],
            ["DENY", "8.8.8.8"],
        ]],
        ["10.0.0.1"],
        ["10.0.0.50"],
        ["10.0.1.1"],
        ["10.1.0.1"],
        ["192.168.1.1"],
        ["172.16.1.1"],
        ["8.8.8.8"],
    ]
    expected = [None, True, False, True, False, False, False, False]
    assert _execute_ops(ops, args) == expected


def test_ops_example_5():
    ops = ["IpFirewall", "allowAccess", "allowAccess", "allowAccess", "allowAccess"]
    args = [
        [[
            ["ALLOW", "0.0.0.0/32"],
            ["ALLOW", "255.255.255.255"],
            ["DENY", "127.0.0.1"],
            ["ALLOW", "192.168.0.0/24"],
            ["DENY", "0.0.0.0/0"],
        ]],
        ["0.0.0.0"],
        ["255.255.255.255"],
        ["127.0.0.1"],
        ["192.168.0.1"],
    ]
    expected = [None, True, True, False, True]
    assert _execute_ops(ops, args) == expected


def test_ops_example_6():
    ops = ["IpFirewall", "allowAccess", "allowAccess", "allowAccess", "allowAccess", "allowAccess"]
    args = [
        [[
            ["ALLOW", "10.0.0.0/31"],
            ["DENY", "10.0.0.4/30"],
            ["ALLOW", "10.0.0.0/8"],
            ["DENY", "0.0.0.0/0"],
        ]],
        ["10.0.0.0"],
        ["10.0.0.1"],
        ["10.0.0.2"],
        ["10.0.0.5"],
        ["10.0.0.8"],
    ]
    expected = [None, True, True, True, False, True]
    assert _execute_ops(ops, args) == expected
