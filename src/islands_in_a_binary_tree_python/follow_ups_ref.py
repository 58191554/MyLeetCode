from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
class Solution:
    def numIslands(self, root: TreeNode) -> int:
        s = set()
        def dfs(node, id):
            nonlocal s
            if node.val == 1:
                if id == -1:
                    s.add(node)
                    nx_id = len(s)
                    if node.left:
                        dfs(node.left, nx_id)
                    if node.right:
                        dfs(node.right, nx_id)
                else:
                    if node.left:
                        dfs(node.left, id)
                    if node.right:
                        dfs(node.right, id)
            else:
                if node.left:
                    dfs(node.left, -1)
                if node.right:
                    dfs(node.right, -1)
        dfs(root, -1)
        def getTreeHash(node):
            q = deque([(node, 0)])
            
            while q:
                size = len(q)
                seq = []
                for _ in range(size):
                    n, pos = q.popleft()
                    if n.left:
                        q.append(n.left, pos - 1)