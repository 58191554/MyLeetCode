IP Firewall
Hard
Bit Manipulation
Interview Stages
Screening
Frequency
Asked By

Last Reported
3 weeks ago
(This question is a variation of the LeetCode question 751. IP to CIDR. If you haven't completed that question yet, it is recommended to solve it first.)

An IP address is a formatted 32-bit unsigned integer where each group of 8 bits is printed as a decimal number and the dot character '.' splits the groups. For example, the binary number 00001111 10001000 11111111 01101011 (spaces added for clarity) formatted as an IP address would be "15.136.255.107".

A CIDR block is a format used to denote a specific set of IP addresses. It is a string consisting of a base IP address, followed by a slash, followed by a prefix length k. The addresses it covers are all the IPs whose first k bits are the same as the base IP address.

Design an IP firewall that determines whether an IPv4 address is allowed or denied based on an ordered list of "ALLOW" or "DENY" rules. Each rule specifies either a single IP or a CIDR block, and only the first matching rule decides the result.

Implement the IpFirewall class:

IpFirewall(List<List<String>> rules) Initializes a firewall with the given list of [action, cidr] rules in priority order.

action is either "ALLOW" or "DENY".
cidr is either an IP (e.g., "1.2.3.4") or a network CIDR (e.g., "192.168.0.0/16").
boolean allowAccess(String ip) Returns true if the ip is allowed by the first rule it matches; otherwise, returns false. It is guaranteed that the ip will match at least one rule.

Constrains

The given IP or CIDR format in the input is always valid.
Example

Input:
["IpFirewall", "allowAccess", "allowAccess", "allowAccess", "allowAccess"]
[[["ALLOW", "192.168.1.100"], ["DENY", "192.168.1.0/24"], ["ALLOW", "192.168.0.0/16"], ["DENY", "0.0.0.0/0"]], ["192.168.1.100"], ["192.168.1.50"], ["192.168.2.10"], ["10.0.0.1"]]
Output:
[null, true, false, true, false]
Explanation:

IpFirewall firewall= new IpFirewall(rules);
firewall.allowAccess("192.168.1.100"); // Returns true. The first rule (["ALLOW", "192.168.1.100"]) matches the specific IP and allows it.
firewall.allowAccess("192.168.1.50"); // Returns false. The second rule (["DENY", "192.168.1.0/24"]) denies the "/24" subnet.
firewall.allowAccess("192.168.2.10"); // Returns true. The third rule (["ALLOW", "192.168.0.0/16"]) allows the broader "/16" subnet.
firewall.allowAccess("10.0.0.1"); // Returns false. The fourth rule (["DENY", "0.0.0.0/0"]]) is the catch-all "DENY".
