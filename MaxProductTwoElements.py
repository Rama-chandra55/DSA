class Solution(object):
    def maxProduct(self, nums):
        lr=sr=float('-inf')
        lr=sr=float('-inf')
        for i in nums:
            if i > lr:
                sr = lr
                lr = i
            elif i > sr:
                sr = i
        res = (lr-1)*(sr-1)
        return res
        
            
        
