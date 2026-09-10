# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def averageOfSubtree(self, root: TreeNode) -> int:
        self.matching_nodes = 0
        
        def traverse(node):
            if not node:

                return 0, 0

            left_sum, left_count = traverse(node.left)
            right_sum, right_count = traverse(node.right)

            current_sum = node.val + left_sum + right_sum
            current_count = 1 + left_count + right_count

            average = current_sum // current_count

            if node.val == average:
                self.matching_nodes += 1

            return current_sum, current_count

        traverse(root)
        return self.matching_nodes
