import math
class Solution(object):
    def sumOfSquares(self, nums):
        n = len(nums)
        add=0
        for i in range(n):
            if n%(i+1) == 0:
                add += nums[i]*nums[i]
        return add

        
