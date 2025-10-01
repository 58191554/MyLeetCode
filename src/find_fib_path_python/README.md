Find Path in Fibonacci Tree
Hard
Binary Tree
Recursion
Interview Stages
Screening
Frequency
Asked By

Last Reported
4 days ago
(This question is a variation of the LeetCode question 2096. Step-By-Step Directions From a Binary Tree Node to Another. If you haven't completed that question yet, it is recommended to solve it first.)

A Fibonacci tree is a binary tree defined recursively. For a tree of order 
n
n (denoted as 
F
n
(
n
)
Fn(n)), the left subtree is 
F
n
(
n
−
2
)
Fn(n−2) and the right subtree is 
F
n
(
n
−
1
)
Fn(n−1). Below is an example of a Fibonacci tree of order 3.


Given a Fibonacci tree of a specific order order, its nodes are labeled in pre-order traversal starting from 0 to n - 1, where n is the total number of nodes in the tree. And given two node labels, source and dest, return the path from source to dest as a string of directional moves:

'L': move from a node to its left child
'R': move from a node to its right child
'U': move from a node to its parent
Constraints:

2 ≤ order≤ 10
0 ≤ source, dest ≤ n - 1
Example 1:

Input: order = 5, source = 5, dest = 7
Output: "UUURL"
Explanation:

The Fibonacci tree of order 5 and its corresponding pre-order labeled version are shown above. The path from node 5 to node 7 is:

5 → parent 3 ("U")
3 → parent 1 ("U")
1 → parent 0 ("U")
0 → right child 6 ("R")
6 → left child 7 ("L")
Example 2:

Input: order = 4, source = 8, dest = 3
Output: "UUULR"

Example 3:

Input: order = 5, source = 4, dest = 13
Output: "UUURRRL"

