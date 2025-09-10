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

def cidr_checklist_II(rules: List[str], cidr: str) -> str:
    s, e = cidr_to_range(cidr)
    status = BEGIN
    cStarts, cEnds = [s], [e]
    for r in rules:
        rStart, rEnd = cidr_to_range(r[1])
        i = 0
        while i < len(cStarts):
            cStart, cEnd = cStarts[i], cEnds[i]
            if cEnd <= rStart or rEnd <= cStart:
                i += 1
                continue
            if status != r[0] and status != BEGIN:
                return DENY
            status = r[0]
            if rStart <= cStart and cEnd <= rEnd:
                cStarts.pop(i)
                cEnds.pop(i)
                continue
            elif cStart < rStart and rEnd < cEnd:
                cEnds[i] = rStart
                cStarts.insert(i + 1, rEnd)
                cEnds.insert(i + 1, cEnd)
            elif cStart < rStart:
                cEnds[i] = rStart
            elif rEnd < cEnd:
                cStarts[i] = rEnd
            i += 1
    return status if status != BEGIN else DENY
    
    