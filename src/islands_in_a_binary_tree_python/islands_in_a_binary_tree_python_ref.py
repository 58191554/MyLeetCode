class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
class Solution:
    def numIslands(self, root: TreeNode) -> int:
        size = 0
        def dfs(node, id):
            nonlocal size
            if node.val == 1:
                if id == -1:
                    size += 1
                    nx_id = size
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
        if root.val == 1:
            size += 1
            dfs(root, 1)
        else:
            dfs(root, -1)
        return size

# class Solution:
#     def numIslands(self, root: TreeNode) -> int:
#         stk = []
#         s = set()
#         cur = root
#         island = False
#         island_id = None
#         while cur:
#             if island == False:
#                 if cur.val == 1:
#                     island = True
#                     island_id = len(s)
#                     s.add(island_id)
#                     if cur.left and cur.right:
                        