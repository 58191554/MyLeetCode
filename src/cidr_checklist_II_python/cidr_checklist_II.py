from typing import List

BEGIN = "BEGIN"
ALLOW = "ALLOW"
DENY = "DENY"

def ip_to_int(ip):
    ip = ip.split(".")
    result = 0
    for i in ip:
        result <<= 8
        result += int(i)
    return result

def cidr_to_range(cidr):
    print(cidr)
    cidr = cidr.split("/")
    ip = ip_to_int(cidr[0])
    if len(cidr) == 1:
        return ip, ip + 1
    mask = int(cidr[1])
    start = (ip >> (32 - mask)) << (32 - mask)
    return start, start + (1 << (32 - mask))

def not_within_range(s, e, l, r):
    return e <= l or r <= s

def cidr_checklist_II(ruls: List[str], cidr: str):
    cidr = cidr_to_range(cidr)
    starts = [cidr[0]]
    ends = [cidr[1]]
    status = BEGIN
    for label, rCidr in ruls:
        left, right = cidr_to_range(rCidr)
        idx = 0
        while idx < len(starts):
            s, e = starts[idx], ends[idx]
            if not_within_range(s, e, left, right):
                idx += 1
                continue
            print("left = {}, right = {}, start = {}, end = {}".format(left, right, s, e))
            if status == DENY or (status != BEGIN and status != label):
                return DENY
            status = label
            if s < left < e:
                ends[idx] = left
                idx += 1
            elif s < right < e:
                starts[idx] = right
                idx += 1
            elif left <= s and e <= right:
                starts.pop(idx)
                ends.pop(idx)
            else:
                ends[idx] = left
                starts.insert(idx + 1, right)
                ends.insert(idx, e)
    return DENY if status == BEGIN else status 