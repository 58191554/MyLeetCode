'''
Task: Given a list of CIDR blocks and a single IP, return whether the IP belongs to any block.

Input
    cidrs: List[str] (e.g., ["10.0.0.0/8","192.168.1.0/24"])
    ip: str (e.g., "192.168.1.42")
    IPv4 only (or state whether IPv6 appears)
Output: True/False
Rule: IP ∈ CIDR if (ip & mask) == (network & mask).
Constraints: 
    1 ≤ N ≤ 10^5 cidrs.
Edge cases: 
    invalid CIDR strings → ignore or return error; leading zeros not allowed; include network/broadcast addresses.
Example:
    cidrs = ["192.168.0.0/16","10.0.0.0/8"], ip = "192.168.1.23" → True
    ip = "172.16.0.1" → False'''
    
from typing import List, Tuple, Optional

class Solution:
    def cidr_white_checklist(self, cidrs: List[str], ip: str):
        def ipToInt(ip: str) -> int:
            ip_arr = list(map(lambda x: int(x), ip.split('.')))
            result = 0
            result += ip_arr[0] << 24
            result += ip_arr[1] << 16
            result += ip_arr[2] << 8
            result += ip_arr[3]
            return result

        def cidrToInterval(cidr: str):
            cidr_arr = cidr.split('/')
            if len(cidr) == 1:
                ip = ipToInt(cidr)
                return ip, ip + 1
            ip = ipToInt(cidr_arr[0])
            mask = 1 << int(cidr_arr[1])
            size = 1 << (32 - mask)
            return ip, ip + size
        
        for rule in cidrs:
            start, end = cidrToInterval(rule[1])
            if start <= ip < end:
                return rule[0] == "ALLOW"
        return False
            