# Follow-up — CIDR Partition & First-Match Justification

Extend the firewall from the base problem (ordered **ALLOW/DENY** rules; IPv4; **first-match-wins**) to support **explainable CIDR decisions**.

## Task

Given:

* An ordered list of rules `rules = [(action, cidr)]` where `action ∈ {"ALLOW","DENY"}` and `cidr` is either an IP (`/32`) or a network prefix.
* A **query CIDR** `Q`.

Produce a **partition** of `Q` into a minimal set of **disjoint CIDR blocks** that exactly cover `Q`, where each block is annotated with:

1. the **final decision** (`ALLOW` or `DENY`) under first-match semantics, and
2. the **index** (0-based) of the **first rule** responsible for that decision (or `-1` if no rule matches and the default is `DENY`).

Return the list sorted by increasing network start address. Adjacent output blocks with the **same decision and same deciding rule index** must be **merged** into a single CIDR when possible.

### Notes

* Rule CIDRs may be **misaligned**; decisions are defined over the exact address set they cover.
* Use **half-open** integer intervals semantics `[start, end)` for IPv4 addresses (0…2³²−1) when reasoning.
* The output must be in **CIDR notation**, using the **fewest** blocks necessary to represent each decided region.

## API (language-agnostic)

```
partitionFirewall(rules, Q) -> List< (cidr, decision, ruleIndex) >
```

* `cidr`: a CIDR string (e.g., `"192.168.1.0/25"`, `"10.0.0.1/32"`).
* `decision`: `"ALLOW"` or `"DENY"`.
* `ruleIndex`: integer; index of the deciding rule for all IPs in `cidr`, or `-1` if unmatched (default deny).

## Constraints

* `1 ≤ |rules| ≤ 2 * 10^5`
* Up to `10^4` queries over the same `rules`.
* Total size of all returned partitions across all queries ≤ `10^6` CIDRs.
* Time and space should be efficient enough to handle the above limits.

## Examples

### Example 1

**Rules**

```
0: ALLOW 192.168.1.100
1: DENY  192.168.1.0/24
2: ALLOW 192.168.0.0/16
3: DENY  0.0.0.0/0
```

**Query**: `192.168.1.0/24`
**Output** (order matters; merge where possible)

```
[
  ("192.168.1.100/32", "ALLOW", 0),
  ("192.168.1.0/32",   "DENY",  1),
  ("192.168.1.1/32",   "DENY",  1),
  ...,
  ("192.168.1.255/32", "DENY",  1)
]
```

(Any equivalent minimal CIDR partition with the same decisions and indices is acceptable.)

### Example 2

**Rules**

```
0: ALLOW 10.0.0.0/9
1: DENY  0.0.0.0/0
```

**Query**: `10.0.0.0/8`
**Output**

```
[
  ("10.0.0.0/9",   "ALLOW", 0),
  ("10.128.0.0/9", "DENY",  1)
]
```

### Example 3

**Rules**

```
0: DENY  192.168.1.128/25
1: ALLOW 192.168.1.0/24
```

**Query**: `192.168.1.0/24`
**Output**

```
[
  ("192.168.1.128/25", "DENY",  0),
  ("192.168.1.0/25",   "ALLOW", 1)
]
```

## Requirements Checklist

* Correct **first-match** precedence.
* Exact coverage of the query; **no gaps, no overlaps**.
* Minimal CIDR representation per decided region; merge adjacent blocks with identical `(decision, ruleIndex)`.
* Scalable to the stated constraints.
