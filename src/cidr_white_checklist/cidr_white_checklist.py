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
        def ip_to_int(ip: str) -> int:
            arr = ip.split(".")
            arr = [int(x) for x in arr]
            return arr[0] * (1 << 24) + arr[1] * (1 << 16) + arr[2] * (1 << 8) + arr[3]
        
        def get_start_end(cidr: str) -> Tuple[int, int]:
            start, size = cidr.split('/')
            start = ip_to_int(start)
            if size == None:
                size = 0
            else:
                size = int(size)
            end = start + (1 << size) - 1
            return start, end
        
        ip_int = ip_to_int(ip)
        print("ip = ", ip_int)
        for cidr in cidrs:
            start, end = get_start_end(cidr)
            print("start = ", start, ", end = ", end)
            if start <= ip_int <= end:
                return True
        return False
            