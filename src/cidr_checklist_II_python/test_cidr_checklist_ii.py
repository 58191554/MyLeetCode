# tests/test_cidr_checklist_ii.py
import pytest

# ---- Import the function under test ----
# Replace this with: from your_module import cidr_checklist_II
from typing import Tuple
from cidr_checklist_II import cidr_checklist_II
ALLOW = "ALLOW"
DENY = "DENY"


R = lambda act, c: (act, c)


def test_sample_rules_behaviour():
    rules = [
        R(ALLOW, "192.168.1.100"),
        R(DENY,  "192.168.1.0/24"),
        R(ALLOW, "192.168.0.0/16"),
        R(DENY,  "0.0.0.0/0"),
    ]
    # Entire /24 contains IPs whose first match is DENY
    assert cidr_checklist_II(rules, "192.168.1.0/24") == DENY
    # Single IP explicitly allowed
    assert cidr_checklist_II(rules, "192.168.1.100") == ALLOW
    # Another IP in the /24 (not the /32) is denied
    assert cidr_checklist_II(rules, "192.168.1.50") == DENY
    # An IP in the broader /16 but outside the denied /24 is allowed
    assert cidr_checklist_II(rules, "192.168.2.10") == ALLOW
    # Catch-all DENY blocks arbitrary other ranges
    assert cidr_checklist_II(rules, "10.0.0.0/8") == DENY


def test_allow_split_covers_whole_query():
    rules = [
        R(ALLOW, "192.168.1.0/25"),
        R(ALLOW, "192.168.1.128/25"),
        R(DENY,  "0.0.0.0/0"),
    ]
    # Two allows fully cover the /24
    assert cidr_checklist_II(rules, "192.168.1.0/24") == ALLOW


def test_partial_allow_then_catchall_deny():
    rules = [
        R(ALLOW, "192.168.1.0/25"),
        R(DENY,  "0.0.0.0/0"),
    ]
    # Only half of the /24 is allowed → not fully covered → DENY
    assert cidr_checklist_II(rules, "192.168.1.0/24") == DENY
    # But the allowed half itself is ALLOW
    assert cidr_checklist_II(rules, "192.168.1.0/25") == ALLOW
    assert cidr_checklist_II(rules, "192.168.1.128/25") == DENY


def test_order_matters_deny_then_broad_allow():
    rules = [
        R(DENY,  "192.168.1.100"),
        R(ALLOW, "192.168.0.0/16"),
    ]
    assert cidr_checklist_II(rules, "192.168.1.100") == DENY
    assert cidr_checklist_II(rules, "192.168.1.101") == ALLOW


def test_mask_normalization_of_rule():
    # Rule base not aligned; should normalize to 192.168.1.0/24
    rules = [R(ALLOW, "192.168.1.5/24")]
    assert cidr_checklist_II(rules, "192.168.1.0/24") == ALLOW
    assert cidr_checklist_II(rules, "192.168.2.0/24") == DENY


@pytest.mark.parametrize(
    "allow_cidr,query,expected",
    [
        ("10.0.0.0/9",  "10.0.0.0/9",  ALLOW),
        ("10.0.0.0/9",  "10.64.0.0/10", ALLOW),   # subset of allowed block
        ("10.0.0.0/9",  "10.128.0.0/9", DENY),    # outside allowed block
    ],
)
def test_subset_vs_outside(allow_cidr, query, expected):
    rules = [R(ALLOW, allow_cidr), R(DENY, "0.0.0.0/0")]
    assert cidr_checklist_II(rules, query) == expected
